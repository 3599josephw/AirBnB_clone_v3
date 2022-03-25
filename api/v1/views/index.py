from flask import jsonify
from api.v1.views import app_views

@app_views.route("/status", methods=['GET'])
def status():
    """Returns Status JSON"""
    return jsonify({'status': 'OK'})