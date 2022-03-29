#!/usr/bin/python3
"""View of a Place - Task 11"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.state import State
from models.state import City
from models.place import Place
from models import storage


@app_views.route("/cities/<city_id>/places", methods=['GET'])
def all_places(city_id):
    """Returns all cities from a State"""
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


# @app_views.route("/states/<city_id>/cities", methods=['POST'])
# def city_create(city_id):
#     """Creates city"""
#     if request.method == 'POST':
#         state = storage.get(State, city_id)
#         if state is None:
#             return abort(404)
#         if not request.json:
#             abort(400, "Not a JSON")
#         if 'name' not in request.json:
#             abort(400, "Missing name")
#         city_dict = request.get_json()
#         city_dict["city_id"] = city_id
#         city = City(**city_dict)
#         city.save()
#         return jsonify(city.to_dict()), 201


# @app_views.route("/cities/<city_id>", methods=['PUT'])
# def city_update(city_id):
#     """Updates a city"""
#     if request.method == 'PUT':
#         if not request.json:
#             abort(400, "Not a JSON")
#         city_dict = request.get_json()
#         city = storage.get(City, city_id)
#         if city is None:
#             return abort(404)
#         for key, value in city_dict.items():
#             if key != 'city_id' and key != 'id' \
#                     and key != 'created_at' and key != 'updated_at':
#                 setattr(city, key, value)
#         storage.save()
#         return jsonify(city.to_dict())
