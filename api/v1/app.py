#!/usr/bin/python3
"""
This module sets up and runs a Flask application for the HBNB API.
It also sets up a CORS policy.

"""

import os

from flask import Flask, make_response
from flask_cors import CORS

from models import storage
from api.v1.views import app_views

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})

app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(exception):
    """Close the storage"""
    storage.close()


@app.errorhandler(404)
def not_found(exception):
    """Return a JSON-formatted 404 response"""
    return make_response({"error": "Not found"}, 404)


if __name__ == '__main__':
    HOST = os.getenv('HBNB_API_HOST', "0.0.0.0")
    PORT = os.getenv('HBNB_API_PORT', 5000)

    app.run(host=HOST, port=PORT, threaded=True)
