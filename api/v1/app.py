#!/usr/bin/python3
from api.v1.views import app_views
from flask import Flask
from models import storage
import os



app = Flask (__name__)

@app.register_blueprint(app_views)
@app.teardown_appcontext
def tearDown():
    """Handles storage calls"""
    storage.close()


if __name__ == "__main__":
    
    PORT = os.getenv("HBNB_API_PORT")
    HOST = os.getenv("HBNB_API_HOST")
   
    if PORT is None:
        PORT =  5000
    if HOST is None:
        HOST = '0.0.0.0'
    app.run(host= HOST, port=HOST)
