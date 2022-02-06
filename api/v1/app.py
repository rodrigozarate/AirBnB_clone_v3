#!/usr/bin/python3
""" API """
from api.v1.views import app_views
from flask import Flask
from models import storage
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={"/*": {"origins": '0.0.0.0'}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """Handles storage calls"""
    storage.close()


if __name__ == "__main__":
    
    PORT = os.getenv("HBNB_API_PORT", '5000')
    HOST = os.getenv("HBNB_API_HOST", '0.0.0.0')
    app.run(host=HOST, port=PORT, threaded=True)
