#!/usr/bin/python3
""" API """
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={"/*": {"origins": '0.0.0.0'}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(self):
    """Handles storage calls"""
    storage.close()


@app.errorhandler(404)
def page_not_found(err):
    """ Return custom 404 error page """
    return jsonify({
        "error": "Not found"
    }), 404


if __name__ == "__main__":
    port = getenv("HBNB_API_PORT", '5000')
    host = getenv("HBNB_API_HOST", '0.0.0.0')
    app.run(host=host, port=port, threaded=True)
