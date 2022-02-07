#!/usr/bin/python3
""" Route States """
from flask import request, abort, jsonify   
from api.v1.app import *
from api.v1.views.index import *
from models.state import State
from models.city import City
from models import storage


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """ show cities """
    new_dict = storage.get(State, state_id)
    new_array = []
    if new_dict:
        for city in new_dict.cities:
            new_array.append(city.to_dict())
        return jsonify(new_array)
    else:
        return abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """ show cities by id """
    new_dict = storage.get(City, city_id)
    if new_dict is None:
        abort(404)
    else:
        return jsonify(new_dict.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """ delete city by id """
    object = storage.get(City, city_id)
    if object is None:
        return abort(404)
    else:
        storage.delete(object)
        storage.save()
        return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """ create a city peñalosa will love it """
    state_dict = storage.get(State, state_id)
    if state_dict is None:
        abort(404)
    try:
        request_data = request.get_json()
    except Exception:
        return abort(400, "Not a JSON")

    if 'name' not in request_data:
        return abort(400, "Missing name")

    information = dict(request_data)
    information['state_id'] = state_id
    new_city = City(**information)
    storage.new(new_city)

    new_json = jsonify(new_city.to_dict())
    storage.save()
    return new_json, 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """ update city info by id"""
    object = storage.get(City, city_id)
    if object is None:
        return abort(404)

    try:
        request_data = request.get_json()
    except Exception:
        return abort(400, "Not a JSON")

    ignore = ["id", "created_at", "updated_at", "state_id"]
    for key, value in dict(request_data).items():
        if key not in ignore:
            setattr(object, key, value)

    new_json = jsonify(object.to_dict())
    storage.save()
    return new_json, 200
