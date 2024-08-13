#!/usr/bin/python3
"""
This module sets up a Flask route to return the status of the application.
It also allows for GET requests to retrieve the number of each object type.
"""

from flask import jsonify
from flasgger import swag_from

from models import storage

from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
@swag_from('documentation/index/status.yml')
def status():
    """ routes to status page """
    return jsonify({'status': 'OK'})


@app_views.route('/stats', methods=['GET'])
@swag_from('documentation/index/get_stats.yml')
def get_stats():
    """ retrieves the number of each objects by type """
    classes = {
        "users": "User",
        "places": "Place",
        "states": "State",
        "cities": "City",
        "amenities": "Amenity",
        "reviews": "Review"
    }

    return jsonify(
        {
            key: storage.count(storage.get_class(value))
            for key, value in classes.items()
        }
    )
