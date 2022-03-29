#!/usr/bin/python3
"""View of a Place - Task 11"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import place
from models.state import State
from models.state import City
from models.place import Place
from models.user import User
from models import storage


@app_views.route("/cities/<city_id>/places", methods=['GET'])
def all_places(city_id):
    """Returns all cities from a State"""
    if request.method == 'GET':
        if city_id is not None:
                city = storage.get(City, city_id)
                if city is not None:
                    place_list = []
                    places = storage.all(Place)
                    for k, v in places.items():
                        if v.city_id == city_id:
                            place_list.append(v.to_dict())
                    return jsonify(place_list)
                else:
                    return abort(404)


@app_views.route("/places/<place_id>", methods=['GET'])
def one_place(place_id=None):
    """Returns a place"""
    if request.method == 'GET':
        if place_id is not None:
            obj = storage.get(Place, place_id)
            if obj is not None:
                return obj.to_dict()
            else:
                return abort(404)


@app_views.route("/places/<place_id>", methods=['DELETE'])
def place_delete(place_id):
    """Deletes a place"""
    if request.method == 'DELETE':
        if place_id:
            obj = storage.get(Place, place_id)
            if obj is not None:
                storage.delete(obj)
                storage.save()
                return {}
            else:
                return abort(404)


@app_views.route("/cities/<city_id>/places", methods=['POST'])
def place_create(city_id):
    """Creates place"""
    if request.method == 'POST':
        city = storage.get(City, city_id)
        if city is None:
            return abort(404)
        if not request.json:
            abort(400, "Not a JSON")
        if 'name' not in request.json:
            abort(400, "Missing name")
        if 'user_id' not in request.json:
            abort(400, "Missing user_id")
        place_dict = request.get_json()
        users = storage.all(User)
        flag = 0
        for k, v in users.items():
            if place_dict["user_id"] == v.id:
                flag = 1
        if flag == 0:
            return abort(404)
        place_dict["city_id"] = city_id
        place = Place(**place_dict)
        place.save()
        return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=['PUT'])
def place_update(place_id):
    """Updates a place"""
    if request.method == 'PUT':
        if not request.json:
            abort(400, "Not a JSON")
        place_dict = request.get_json()
        place = storage.get(Place, place_id)
        if place is None:
            return abort(404)
        for key, value in place_dict.items():
            if key != 'city_id' and key != 'id' and key != 'user_id' \
                    and key != 'created_at' and key != 'updated_at':
                setattr(place, key, value)
        storage.save()
        return jsonify(place.to_dict())
