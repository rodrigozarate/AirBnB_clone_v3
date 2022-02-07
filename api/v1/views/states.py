#!/usr/bin/python3
""" Handles all default RESTFul API """
from api.v1.views.index import *
from api.v1.app import *
from flask import jsonify, abort, request
from models.state import State


@app_views.route('/states', strict_slashes=False)
def states():
    """ Retrieves the list of all State objects """
    states_list = storage.all(State)
    states = []
    for s in states_list:
        s.append(s.to_dict())
    return jsonify(states)


@app_views.route('/states/<state_id>', strict_slashes=False)
def state_id(state_id):
    """ Retrieves a State object with state id """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', method=['DELETE'],
                 strict_slashes=False)
def state_id(state_id):
    """ Deletes a State object """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        storage.delete(state)
        return jsonify({}), 200


@app_views.route('/states', method=['POST'], strict_slashes=False)
def create_states():
    """ Creates a State """
    new_object = request.get_json()
    if new_object is None:
        abort(400, "Not a JSON")
    else:
        name = new_object.get('name', None)
        if name is None:
            abort(400, "Missing name")
        obj = State(new_object)
        obj.save()
        return jsonify(obj.to_dict()), 201


@app_views.route('/states/<state_id>', method=['PUT'],
                 strict_slashes=False)
def update_states(state_id):
    """ Update a State """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        data = request.get_json()
        ignore = ['id', 'created_at', 'updated_at']
        if data is None:
            abort(400, "Not a JSON")
        else:
            for key, value in data.items():
                if key not in ignore:
                    setattr(state, key, value)
            storage.save()
            return jsonify(state.to_dict()), 200
