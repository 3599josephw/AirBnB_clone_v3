#!/usr/bin/python3
"""View of a Place - Task 11"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import place
from models.state import State
from models.state import City
from models.place import Place
from models.user import User
from models.review import Review
from models import storage


@app_views.route("/places/<place_id>/reviews", methods=['GET'])
def all_reviews(place_id):
    """Returns all Reviews from a Place"""
    if request.method == 'GET':
        if place_id is not None:
                place = storage.get(Place, place_id)
                if place is not None:
                    review_list = []
                    reviews = storage.all(Review)
                    for k, v in reviews.items():
                        if v.place_id == place_id:
                            review_list.append(v.to_dict())
                    return jsonify(review_list)
                else:
                    return abort(404)


@app_views.route("/reviews/<review_id>", methods=['GET'])
def one_review(review_id=None):
    """Returns a review"""
    if request.method == 'GET':
        if review_id is not None:
            obj = storage.get(Review, review_id)
            if obj is not None:
                return obj.to_dict()
            else:
                return abort(404)


@app_views.route("/reviews/<review_id>", methods=['DELETE'])
def review_delete(review_id):
    """Deletes a review"""
    if request.method == 'DELETE':
        if review_id:
            obj = storage.get(Review, review_id)
            if obj is not None:
                storage.delete(obj)
                storage.save()
                return {}
            else:
                return abort(404)


@app_views.route("/places/<place_id>/reviews", methods=['POST'])
def review_create(place_id):
    """Creates review"""
    if request.method == 'POST':
        place = storage.get(Place, place_id)
        if place is None:
            return abort(404)
        if not request.json:
            abort(400, "Not a JSON")
        if 'user_id' not in request.json:
            abort(400, "Missing user_id")
        if 'text' not in request.json:
            abort(400, "Missing text")
        review_dict = request.get_json()
        users = storage.all(User)
        flag = 0
        for k, v in users.items():
            if review_dict["user_id"] == v.id:
                flag = 1
        if flag == 0:
            return abort(404)
        review_dict["place_id"] = place_id
        review = Review(**review_dict)
        review.save()
        return jsonify(review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=['PUT'])
def review_update(review_id):
    """Updates a review"""
    if request.method == 'PUT':
        if not request.json:
            abort(400, "Not a JSON")
        review_dict = request.get_json()
        review = storage.get(Review, review_id)
        if review is None:
            return abort(404)
        for key, value in review_dict.items():
            if key != 'place_id' and key != 'id' and key != 'user_id' \
                    and key != 'created_at' and key != 'updated_at':
                setattr(review, key, value)
        storage.save()
        return jsonify(review.to_dict())
