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
    classes = {'Amenity': 'amenities', 'City': 'cities', 'Place': 'places', 'Review': 'reviews',
               'State': 'states', 'User': 'users'}
    dict = {}
    for k, v in classes.items():
        num = storage.count(k)
        dict[v] = num
    return dict
