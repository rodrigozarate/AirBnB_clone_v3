#!/usr/bin/python3
"""Blueprint and routes"""
from flask import request
from api.v1.views.index import *
from api.v1.app import *
from models.place import Place
from models.city import City
import copy
import json


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places_city(city_id):
    """Return json file with all places"""
    object = storage.get(City, city_id)
    new_array = []
    if object is None:
        return error_handler_404(object)
    for object_place in object.places:
        new_array.append(object_place.to_dict())
    return json.dumps(new_array)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """Return json file of object place, filtered with id"""
    new_dict = storage.get(Place, place_id)
    if new_dict is None:
        return error_handler_404(new_dict)
    return json.dumps(new_dict.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Delete an object place by id"""
    object = storage.get(Place, place_id)
    if object is None:
        return error_handler_404(object)
    storage.delete(object)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Create a new object place"""
    object_city = storage.get(City, city_id)
    if object_city is None:
        return error_handler_404(object_city)
    try:
        request_data = request.get_json()
    except Exception:
        return error_handler_400("Not a JSON")
    dict_info_place = dict(request_data)
    if 'user_id' not in dict_info_place.keys():
        return error_handler_400("Missing user_id")
    object_user = storage.get(User, dict_info_place['user_id'])
    if object_user is None:
        return error_handler_404(object)
    if 'name' not in request_data:
        return error_handler_400("Missing name")
    dict_info_place['city_id'] = city_id
    new_object = Place(**dict_info_place)
    storage.new(new_object)
    storage.save()
    return json.dumps(new_object.to_dict()), 201


@app_views.route('/places_search', methods=['POST'],
                 strict_slashes=False)
def places_search():
    """Create a new object place"""
    try:
        request_data = request.get_json()
    except Exception:
        return error_handler_400("Not a JSON")
    new_array = []
    if (str(request_data) == "{}" or
        ('states' in request_data.keys() and
         str(request_data['states']) == '[]' and
         'cities' in request_data.keys() and
         str(request_data['cities']) == '[]')):
        objects_place = storage.all(Place)
        if ('amenities' in request_data.keys() and
                str(request_data['amenities']) != '[]'):
            for place in objects_place.values():
                validator = False
                for amenity in place.amenities:
                    if amenity.id in list(request_data['amenities']):
                        validator = True
                if validator:
                    del place.__dict__['amenities']
                    new_array.append(place.to_dict())
        else:
            for place in objects_place.values():
                new_array.append(place.to_dict())
        return json.dumps(new_array)
    else:
        no_ignore = ["states", "cities"]
        subquery = ''
        for key, val in request_data.items():
            if key in no_ignore:
                for ids in val:
                    if key == 'states':
                        subquery = (storage._DBStorage__session.query(City.id).
                                    join(State, City.state_id == State.id).
                                    filter(State.id == "{}".format(ids)).
                                    subquery())
                    else:
                        subquery = val
                    query = (storage._DBStorage__session.query(Place).
                             filter(Place.city_id.in_(subquery)))
                    if ('amenities' in request_data.keys() and
                            str(request_data['amenities']) != '[]'):
                        for place in query:
                            validator = False
                            for amenity in place.amenities:
                                if (amenity.id in
                                        list(request_data['amenities'])):
                                    validator = True
                            if validator:
                                del place.__dict__['amenities']
                                new_array.append(place.to_dict())
                    else:
                        for object_places in query:
                            place_dict = object_places.to_dict()
                            if place_dict not in new_array:
                                new_array.append(place_dict)
                    if type(subquery) is list:
                        break
    if 'amenities' in request_data.keys():
        if request_data['amenities'] == '':
            return json.dumps(new_array)
    return json.dumps(new_array)


@ app_views.route('/places/<place_id>', methods=['PUT'],
                  strict_slashes=False)
def update_place(place_id):
    """Update information of an object place by id"""
    object = storage.get(Place, place_id)
    if object is None:
        return error_handler_404(object)
    try:
        request_data = request.get_json()
    except Exception:
        return error_handler_400("Not a JSON")
    ignore = ["id", "user_id", "city_id", "created_at", "updated_at"]
    for key, value in dict(request_data).items():
        if key not in ignore:
            setattr(object, key, value)
    new_json = json.dumps(object.to_dict())
    storage.save()
    return new_json, 200
