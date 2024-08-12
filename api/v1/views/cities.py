#!/usr/bin/python3
"""
This module sets up Flask routes for City objects. It allows for
GET, POST, PUT, and DELETE requests.

- GET requests return a JSON list of all City objects in a State,
a JSON representation of a City object, or a 404 error if
the City object does not exist.

- POST requests create a new City object. PUT requests update a City object.
a 400 error is returned if the request is not JSON formatted or
if the JSON body is missing a name key.

- DELETE requests delete a City object. All responses are JSON formatted.
a 404 error is returned if the City object does not exist.

- PUT requests update a City object. A 404 error is returned
if the City object does not exist or if the request is not JSON formatted

DELETE requests are expected to have an empty JSON body.

GET requests do not require a JSON body.

The following routes are defined:
GET /states/<state_id>/cities
GET /cities/<city_id>
DELETE /cities/<city_id>
POST /states/<state_id>/cities
PUT /cities/<city_id>

The following error codes are returned:
404: Not found
400: Not a JSON
400: Missing name
200: OK
201: Created
"""
from flask import jsonify, abort, request
from models.state import State
from models.city import City
from models import storage
from api.v1.views import app_views


@app_views.route("/states/<state_id>/cities/", methods=["GET"])
def get_cities(state_id):
    """Return a JSON list of all City objects in a State"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    return jsonify([
        city.to_dict()
        for city in state.cities
    ])


@app_views.route("/cities/<city_id>", methods=["GET"])
def get_city(city_id):
    """Return a JSON representation of a City object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"])
def delete_city(city_id):
    """Delete a City object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    city.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities/", methods=["POST"])
def post_city(state_id):
    """Create a new City object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    city_data = request.get_json(silent=True)
    if not city_data:
        abort(400, "Not a JSON")
    if "name" not in city_data:
        abort(400, "Missing name")

    new_city = City(name=city_data.get("name"), state_id=state_id)
    new_city.save()

    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"])
def put_city(city_id):
    """Update a City object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    city_data = request.get_json(silent=True)
    if not city_data:
        abort(400, "Not a JSON")

    city.update(**city_data)
    city.save()

    return jsonify(city.to_dict()), 200
