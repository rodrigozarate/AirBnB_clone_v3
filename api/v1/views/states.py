#!/usr/bin/python3
""" Handles all default RESTFul API """
from flask import request, abort, jsonify
from api.v1.app import *
from api.v1.views.index import *
from models.state import State
from models import storage


def validate(ref_id):
    """ validate if query have id to reference """
    try:
        valid = storage.get(obj, ref_id)
        valid.to_dict()
    except Exception:
        abort(404)
    return valid


def get_all_states(id_state):
    """ get all states """
    if id_state is not None:
        state = validate(id_state)
        dict_state = state.to_dict()
        return jsonify(dict_state)
    states = storage.all(State)
    states_all = []
    for state in states.values():
        states_all.append(state.to_dict())
    return jsonify(states_all)


def delete_state(id_state):
    """ delete state request """
    state = validate(id_state)
    storage.delete(state)
    storage.save()
    response = {}
    return jsonify(response)


def create_state(request):
    """ create state """
    request_json = request.get_json()
    if request_json is None:
        abort(400, 'Not a JSON')
    try:
        name_state = request_json['name']
    except Exception:
        abort(400, "Missing name")
    state = State(name=name_state)
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict())


def update_state(state_id, request):
    """ update state """
    state = validate(state_id)
    request_json = request.get_json()
    if request_json is None:
        abort(400, 'Not a JSON')
    for key, value in request_json.items():
        if (key not in ('id', 'created_at', 'updated_at')):
            setattr(state, key, value)
        storage.save()
        return jsonify(state.to_dict())


@app_views.route('/states/', methods=['GET', 'POST'],
                 defaults={'state_id': None}, strict_slashes=False)
@app_views.route('/states/<state_id>',
                 methods=['GET', 'DELETE', 'PUT'])
def states(state_id):
    """ Switch to select function """
    if (request.method == "GET"):
        return get_all_states(state_id)
    elif request.method == "DELETE":
        return delete_state(state_id)
    elif request.method == "POST":
        return create_state(request), 201
    elif request.method == 'PUT':
        return update_state(state_id, request), 200
