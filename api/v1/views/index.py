#!/usr/bin/python3
"""Returns json status OK"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route("/status", methods=['GET'])
def status():
    """Returns Status JSON"""
    return jsonify({'status': 'OK'})


@app_views.route("/stats", methods=['GET'])
def count():
    """Returns count of object"""
    classes = ['amenities', 'cities', 'places', 'reviews',
               'states', 'users']
    dict = {}
    for cls in classes:
        num = storage.count(cls)
        dict[cls] = num
    return dict
