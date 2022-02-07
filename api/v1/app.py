#!/usr/bin/python3
""" API """
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources={"/*": {"origins": '0.0.0.0'}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """Handles storage calls"""
    storage.close()


@app.errorhandler(404)
def page_not_found(err):
    return jsonify({
        "error": "Not found"
    }), 404


if __name__ == "__main__":
    PORT = getenv("HBNB_API_PORT", '5000')
    HOST = getenv("HBNB_API_HOST", '0.0.0.0')
    app.run(host=HOST, port=PORT, threaded=True)
