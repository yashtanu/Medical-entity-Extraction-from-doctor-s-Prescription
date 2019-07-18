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


class ImgtoText(object):
    def __init__(self):
        self.subscription_key = "6ea099736b8e4706a1dc673b40c1c4a0"
        assert self.subscription_key
        self.vision_base_url = "https://centralindia.api.cognitive.microsoft.com/vision/v2.0/"
        self.text_recognition_url = self.vision_base_url + "recognizeText"




    def process(self,image_url):
# Set image_url to the URL of an image that you want to analyze
        entity_list = []
        headers = {'Ocp-Apim-Subscription-Key': self.subscription_key}
# Note: The request parameter changed for APIv2.
# For APIv1, it is 'handwriting': 'true'.
        params  = {'mode': 'Handwritten'}
        data    = {'url': image_url}
        response = requests.post(
            self.text_recognition_url, headers=headers, params=params, json=data)
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
        for polygon in polygons:
            vertices = [(polygon[0][i], polygon[0][i+1])
                for i in range(0, len(polygon[0]), 2)]
            text     = polygon[1]
#             print(text)
            
            client = boto3.client(service_name='comprehendmedical', region_name='us-east-1')
            result = client.detect_entities(Text= text)
            entities = result['Entities'];
            for entity in entities:
                entity_list.append(entity)
        print(entity_list)
       
        
    

if __name__ == '__main__':
    img_url="http://4.bp.blogspot.com/-xqaGZBu0tao/TmD-p7ZT9eI/AAAAAAAAAAQ/Ur0w5cnh3Fc/s1600/MEDICAL+PRESCRIPTION.jpg"
    ImgtoText = ImgtoText()
    ImgtoText.process(img_url)
    


import pandas as pd
all_data = []
for ele in new:
    dict_data = {}
#     print(ele.keys())
#     print(ele.get("Text"))
#     print(ele.get("Category"))
#     print(ele.get("Type"))
    dict_data["Text"] = ele.get("Text")
    dict_data["Category"] = ele.get("Category")
    dict_data["Type"] = ele.get("Type")
#     print(dict_data)
    all_data.append(dict_data)
# print(all_data)
dataframe = pd.DataFrame()
dataframe = dataframe.append(all_data)
dataframe = dataframe[['Text', 'Type','Category']]
dataframe1=dataframe.style.set_properties(**{'text-align': 'left'})
dataframe1
