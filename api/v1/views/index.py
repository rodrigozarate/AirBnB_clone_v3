from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status', strict_slashes=False)
def status():
    """ Return a status of Flask view """
    my_dict = {"status": "OK"}
    return jsonify(my_dict)
