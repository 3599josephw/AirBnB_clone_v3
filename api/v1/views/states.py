#!/usr/bin/python3
"""View of a State - Task 7"""
from flask import jsonify
from api.v1.app import app
from api.v1.views import app_views
from models.state import State
from models import storage

@app_views.route("/states", methods=['GET'])
def states():
    """Returns a list of all States"""
    #the below code doesn't work, but it's a starting point? maybe?
    #feel free to do edit/delete. im preeeeetty sure
    #we're supposed to jsonify() it, but idk man
    #the second working resource link kinda helps
    states = storage.all(State)
    statelist = []
    for state in states.values():
        statelist.append(state.to_dict())
    return jsonify(statelist)
