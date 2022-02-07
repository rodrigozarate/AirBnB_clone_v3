#!/usr/bin/python3
"""
   New Review object that handles all
   default RESTFul API actions
"""
from flask import request, abort
from api.v1.app import *
from api.v1.views.index import *
from models.review import Review
import json


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_place_reviews(place_id):
    """Return json file with all REVIEWS"""
    new_dict = storage.get('Place', place_id)
    new_array = []
    if new_dict:
        for review in new_dict.reviews:
            new_array.append(review.to_dict())
        return json.dumps(new_array)
    else:
        abort(404)

@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Return json file of object Review, filtered with id"""
    new_dict = storage.get(Review, review_id)
    if new_dict is None:
        return abort(404)
    else:
        return json.dumps(new_dict.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Delete an object Review by id"""
    object = storage.get(Review, review_id)
    if object is None:
        abort(404)
    else:
        storage.delete(object)
        storage.save()
        return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """Create a new object Review"""
    place_dict = storage.get('Place', place_id)
    if place_dict is None:
        abort(404)

    try:
        request_data = request.get_json()
    except Exception:
        abort(400, "Not a JSON")

    if 'user_id' not in request_data:
        abort(400, "Missing user_id")

    user_dict = storage.get('User', request_data['user_id'])
    if user_dict is None:
        abort(404)

    if 'text' not in request_data:
        abort(400, "Missing text")

    information = dict(request_data)
    information['place_id'] = place_id
    new_review = Review(**information)
    storage.new(new_review)

    new_json = json.dumps(new_review.to_dict())
    storage.save()
    return new_json, 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Update information of an object Review by id"""
    object = storage.get(Review, review_id)
    if object is None:
        abort(404)

    try:
        request_data = request.get_json()
    except Exception:
        abort(400, "Not a JSON")

    ignore = ["id", "created_at", "updated_at", "user_id", "place_id"]
    for key, value in dict(request_data).items():
        if key not in ignore:
            setattr(object, key, value)

    new_json = json.dumps(object.to_dict())
    storage.save()
    return new_json, 200
