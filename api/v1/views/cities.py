#!/usr/bin/python3
"""
This module sets up Flask routes for City objects. It allows for
GET, POST, PUT, and DELETE requests.
"""
from flask import jsonify, abort, request
from flasgger import swag_from

from models.state import State
from models.city import City
from models import storage
from api.v1.views import app_views


@app_views.route("/states/<state_id>/cities/", methods=["GET"])
@swag_from("documentation/city/cities_by_state.yml")
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
@swag_from("documentation/city/get_city.yml")
def get_city(city_id):
    """Return a JSON representation of a City object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"])
@swag_from("documentation/city/delete_city.yml")
def delete_city(city_id):
    """Delete a City object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    city.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities/", methods=["POST"])
@swag_from("documentation/city/post_city.yml")
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
@swag_from("documentation/city/put_city.yml")
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
