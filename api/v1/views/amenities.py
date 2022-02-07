#!/usr/bin/python3
""" route amenities """
from flask import request
from api.v1.app import *
from api.v1.views.index import *
from models.amenity import *
import json


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """ Return all amenities """
    new_dict = storage.all(Amenity)
    new_array = []
    for object in new_dict.values():
        new_array.append(object.to_dict())
    return json.dumps(new_array)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """ filter amenity by id"""
    new_dict = storage.get(Amenity, amenity_id)
    if new_dict is None:
        return error_handler_404(new_dict)
    return json.dumps(new_dict.to_dict()), 200


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ delete amenity by id """
    object = storage.get(Amenity, amenity_id)
    if object is None:
        return error_handler_404(object)
    storage.delete(object)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """ create amenity """
    try:
        request_data = request.get_json()
    except Exception:
        return error_handler_400("Not a JSON")
    if 'name' not in request_data:
        return error_handler_400("Missing name")
    info_amenity = dict(request_data)
    new_amenity = Amenity(**info_amenity)
    storage.new(new_amenity)
    new_json = json.dumps(new_amenity.to_dict())
    storage.save()
    return new_json, 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """ update amenity by id """
    object = storage.get(Amenity, amenity_id)
    if object is None:
        return error_handler_404(object)
    try:
        request_data = request.get_json()
    except Exception:
        return error_handler_400("Not a JSON")
    ignore = ["id", "created_at", "updated_at"]
    for key, value in dict(request_data).items():
        if key not in ignore:
            setattr(object, key, value)
    new_json = json.dumps(object.to_dict())
    storage.save()
    return new_json, 200
