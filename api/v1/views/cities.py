#!/usr/bin/python3
"""View of a City - Task 8"""
from flask import jsonify, request, abort
from api.v1.app import not_found
from api.v1.views import app_views
from models.state import State
from models.state import City
from models import storage


@app_views.route("/states/<state_id>/cities", methods=['GET'])
def all_cities(state_id):
    """Returns all cities from a State"""
    if state_id is not None:
            state = storage.get(State, state_id)
            if state is not None:
                cities_list = []
                for city in state.cities:
                    cities_list.append(city.to_dict())
                return jsonify(cities_list)
            else:
                return not_found(404)

    """states = storage.all(State)
    statelist = []
    for state in states.values():
        statelist.append(state.to_dict())
    return jsonify(statelist)"""


@app_views.route("/cities/<city_id>", methods=['GET'])
def one_city(city_id=None):
    """Returns a city"""
    if request.method == 'GET':
        if city_id is not None:
            obj = storage.get(City, city_id)
            if obj is not None:
                return obj.to_dict()
            else:
                return not_found(404)


@app_views.route("/cities/<city_id>", methods=['DELETE'])
def city_delete(city_id):
    """Deletes a city"""
    if city_id:
        obj = storage.get(City, city_id)
        if obj is not None:
            storage.delete(obj)
            storage.save()
            return {}
        else:
            return not_found(404)


@app_views.route("/states/<state_id>/cities", methods=['POST'])
def city_create(state_id):
    """Creates city"""
    if request.method == 'POST':
        state = storage.get(State, state_id)
        if state is None:
            return not_found(404)
        if not request.json:
            abort(400, "Not a JSON")
        if 'name' not in request.json:
            abort(400, "Missing name")
        city_dict = request.get_json()
        city_dict["state_id"] = state_id
        city = City(**city_dict)
        city.save()
        return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=['PUT'])
def city_update(city_id):
    """Updates a city"""
    if request.method == 'PUT':
        if not request.json:
            abort(400, "Not a JSON")
        city_dict = request.get_json()
        city = storage.get(City, city_id)
        if city is None:
            return not_found(404)
        for key, value in city_dict.items():
            if key != 'state_id' and key != 'id' \
                    and key != 'created_at' and key != 'updated_at':
                setattr(city, key, value)
        storage.save()
        return jsonify(city.to_dict())
