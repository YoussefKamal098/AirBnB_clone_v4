#!/usr/bin/python3
"""
This module sets up and runs a Flask application for the HBNB API.
It also sets up a CORS policy. and a Swagger documentation route at /apidocs.
It also handles 404 errors.
"""

import os

from flask import Flask, make_response, jsonify
from flask_cors import CORS
from flasgger import Swagger
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

# Set the JSONIFY_PRETTYPRINT_REGULAR config to True for pretty JSON output
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Set the SWAGGER config for the API documentation
app.config['SWAGGER'] = {
    'title': 'AirBnB clone Restful API',
    'uiversion': 3
}

# CORS policy for all routes in the API (i.e. /api/*) from all origins (i.e. *)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})

# Swagger documentation setup for the API at /apidocs
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}

# Initialize the Swagger documentation for the API at /apidocs
swagger = Swagger(app, config=swagger_config)

# Set the URL map to not require trailing slashes
app.url_map.strict_slashes = False

# Register the blueprint for the API routes
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(exception):
    """Close the storage"""
    storage.close()


@app.errorhandler(404)
def not_found(exception):
    """Return a JSON-formatted 404 response"""
    return make_response(jsonify({
        "error": "Not found", 'message': str(exception)
    }), 404)


@app.errorhandler(400)
def bad_request(exception):
    """Return a JSON-formatted 400 response"""
    return make_response(jsonify({
        'error': 'Bad Request', 'message': str(exception)
    }), 400)


if __name__ == '__main__':
    HOST = os.getenv('HBNB_API_HOST', "0.0.0.0")
    PORT = os.getenv('HBNB_API_PORT', 5000)

    app.run(host=HOST, port=PORT, threaded=True, debug=True)
