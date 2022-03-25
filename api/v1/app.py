#!/usr/bin/python3
"""Task 4 - """
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import environ


app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(appcontext):
    """shuts down the database"""
    storage.close()

if __name__ == '__main__':
    if environ.get('HBNB_API_HOST') is not None:
        host = environ.get('HBNB_API_HOST')
    else:
        host = "0.0.0.0"
    if environ.get('HBNB_API_PORT') is not None:
        port = environ.get('HBNB_API_PORT')
    else:
        port = "5000"

    app.run(host=host, port=port, threaded=True)
