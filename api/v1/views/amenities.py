#!/usr/bin/python3
"""View of an Amenity - Task 9"""
from flask import jsonify, request, abort
from api.v1.app import not_found
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage


@app_views.route("/amenities", methods=['GET'])
def all_amenities():
    """Returns all amenities"""
    amenities = storage.all(Amenity)
    amenitylist = []
    for amenity in amenities.values():
        amenitylist.append(amenity.to_dict())
    return jsonify(amenitylist)


@app_views.route("/amenities/<amenity_id>", methods=['GET'])
def one_amenity(amenity_id=None):
    """Returns one Amenity"""
    if request.method == 'GET':
        if amenity_id is not None:
            obj = storage.get(Amenity, amenity_id)
            if obj is not None:
                return obj.to_dict()
            else:
                return not_found(404)


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'])
def amenity_delete(amenity_id):
    """Deletes an Amenity"""
    if amenity_id:
        obj = storage.get(Amenity, amenity_id)
        if obj is not None:
            storage.delete(obj)
            storage.save()
            return {}
        else:
            return not_found(404)


@app_views.route("/amenities", methods=['POST'])
def amenity_create():
    """Creates amenity"""
    if request.method == 'POST':
        if not request.json:
            abort(400, "Not a JSON")
        if 'name' not in request.json:
            abort(400, "Missing name")
        amenity_dict = request.get_json()
        amenity = Amenity(**amenity_dict)
        amenity.save()
        return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=['PUT'])
def amenity_update(amenity_id):
    """Updates an amenity"""
    if request.method == 'PUT':
        if not request.json:
            abort(400, "Not a JSON")
        amenity_dict = request.get_json()
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            return not_found(404)
        for key, value in amenity_dict.items():
            if key != 'id' and key != 'created_at' and key != 'updated_at':
                setattr(amenity, key, value)
        storage.save()
        return jsonify(amenity.to_dict())
