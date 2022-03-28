#!/usr/bin/python3
"""View of a State - Task 7"""
from flask import jsonify
from api.v1.app import not_found
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route("/states", methods=['GET'])
@app_views.route("/states/<state_id>", methods=['GET'])
def states(state_id=None):
    """Returns a list of all States"""
    states = storage.all(State)
    if state_id:
        obj = storage.get(State, state_id)
        if obj is not None:
            return obj.to_dict()
        else:
            return not_found(404)
    else:
        statelist = []
        for state in states.values():
            statelist.append(state.to_dict())
        return jsonify(statelist)


