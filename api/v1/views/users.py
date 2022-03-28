#!/usr/bin/python3
"""View of a user - Task 10"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.user import User
from models import storage


@app_views.route("/users", methods=['GET'])
def all_users():
    """Returns all users"""
    users = storage.all(User)
    userlist = []
    for user in users.values():
        userlist.append(user.to_dict())
    return jsonify(userlist)


@app_views.route("/users/<user_id>", methods=['GET'])
def one_user(user_id=None):
    """Returns a user"""
    if request.method == 'GET':
        if user_id is not None:
            obj = storage.get(User, user_id)
            if obj is not None:
                return obj.to_dict()
            else:
                return abort(404)


@app_views.route("/users/<user_id>", methods=['DELETE'])
def user_delete(user_id):
    """Deletes a User"""
    if user_id:
        obj = storage.get(User, user_id)
        if obj is not None:
            storage.delete(obj)
            storage.save()
            return {}
        else:
            return abort(404)


@app_views.route("/users", methods=['POST'])
def user_create():
    """Creates user"""
    if request.method == 'POST':
        if not request.json:
            abort(400, "Not a JSON")
        if 'email' not in request.json:
            abort(400, "Missing email")
        if 'password' not in request.json:
            abort(400, "Missing password")
        user_dict = request.get_json()
        user = User(**user_dict)
        user.save()
        return jsonify(user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=['PUT'])
def user_update(user_id):
    """Updates a user"""
    if request.method == 'PUT':
        if not request.json:
            abort(400, "Not a JSON")
        user_dict = request.get_json()
        user = storage.get(User, user_id)
        if user is None:
            return abort(404)
        for key, value in user_dict.items():
            if key != 'email' and key != 'id' and \
                    key != 'created_at' and key != 'updated_at':
                setattr(user, key, value)
        storage.save()
        return jsonify(user.to_dict())
