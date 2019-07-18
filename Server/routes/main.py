from flask import Blueprint, jsonify, request
# from __init__ import mongo
import requests
import time
#%matplotlib inline
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from PIL import Image
from io import BytesIO
import pandas as pd
import boto3
import json
import pandas as pd

main = Blueprint('main', __name__)

def process(image_url):
  subscription_key = "6ea099736b8e4706a1dc673b40c1c4a0"
  assert subscription_key
  vision_base_url = "https://centralindia.api.cognitive.microsoft.com/vision/v2.0/"
  text_recognition_url = vision_base_url + "recognizeText"
# Set image_url to the URL of an image that you want to analyze
  entity_list = []
  print(subscription_key)
  headers = {'Ocp-Apim-Subscription-Key': subscription_key}
# Note: The request parameter changed for APIv2.
# For APIv1, it is 'handwriting': 'true'.
  params  = {'mode': 'Handwritten'}
  data    = {'url': image_url}
  response = requests.post(
      text_recognition_url, headers=headers, params=params, json=data)
  response.raise_for_status()

# Extracting handwritten text requires two API calls: One call to submit the
# image for processing, the other to retrieve the text found in the image.

# Holds the URI used to retrieve the recognized text.
  operation_url = response.headers["Operation-Location"]

# The recognized text isn't immediately available, so poll to wait for completion.
  analysis = {}
  poll = True
  while (poll):
      response_final = requests.get(
          response.headers["Operation-Location"], headers=headers)
      analysis = response_final.json()
      time.sleep(1)
      if ("recognitionResult" in analysis):
          poll= False 
      if ("status" in analysis and analysis['status'] == 'Failed'):
          poll= False

  polygons=[]
  if ("recognitionResult" in analysis):
# Extract the recognized text, with bounding boxes.
      polygons = [(line["boundingBox"], line["text"])
          for line in analysis["recognitionResult"]["lines"]]

# Display the image and overlay it with the extracted text.
  plt.figure(figsize=(15, 15))
  image = Image.open(BytesIO(requests.get(image_url).content))
  ax = plt.imshow(image)
  text = ''
  for polygon in polygons:
      vertices = [(polygon[0][i], polygon[0][i+1])
          for i in range(0, len(polygon[0]), 2)]
      text += polygon[1]
#             print(text)
      
      client = boto3.client(service_name='comprehendmedical', region_name='us-east-1')
      result = client.detect_entities(Text= text)
      entities = result['Entities'];
      for entity in entities:
          entity_list.append(entity)
  return jsonify(text= text, entity_list= entity_list)


@main.route('/')
def index():
    # user_cursor = mongo.db.User.find()
    # user_list = [doc for doc in user_cursor]
    # return jsonify(data = user_list)
    img_url = request.args.get('url')
    # img_url="http://4.bp.blogspot.com/-xqaGZBu0tao/TmD-p7ZT9eI/AAAAAAAAAAQ/Ur0w5cnh3Fc/s1600/MEDICAL+PRESCRIPTION.jpg"
    entity_data = process(img_url)
    print(entity_data)
    return entity_data