from flask import Flask
from routes.main import main
from __init__ import app

app.register_blueprint(main, url_prefix='/api/main/get')

@app.route('/')
def main():
    return 'Welcome to Flask demo'

if(__name__) == '__main__':
    app.run()