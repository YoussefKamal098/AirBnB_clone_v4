#!/usr/bin/python3
"""
This module sets up a Flask route to return a JSON list of all Amenity objects.
It also allows for GET, POST, PUT, and DELETE requests.
"""
from flask import jsonify, abort, request
from flasgger import swag_from

from models import storage
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route("/amenities", methods=["GET"])
@swag_from('documentation/amenity/all_amenities.yml')
def get_amenities():
    """Return a JSON list of all Amenity objects"""
    return jsonify([
        amenity.to_dict()
        for amenity in storage.all(Amenity).values()
    ])


@app_views.route("/amenities/<amenity_id>", methods=["GET"])
@swag_from('documentation/amenity/get_amenity.yml')
def get_amenity(amenity_id):
    """Return a JSON representation of an Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"])
@swag_from('documentation/amenity/delete_amenity.yml')
def delete_amenity(amenity_id):
    """Delete an Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    amenity.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route("/amenities/", methods=["POST"])
@swag_from('documentation/amenity/post_amenity.yml')
def post_amenity():
    """Create a new Amenity object"""
    amenity_data = request.get_json(silent=True)

    if not amenity_data:
        abort(400, "Not a JSON")
    if "name" not in amenity_data:
        abort(400, "Missing name")

    new_amenity = Amenity(name=amenity_data.get("name"))
    new_amenity.save()

    return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"])
@swag_from('documentation/amenity/put_amenity.yml')
def put_amenity(amenity_id):
    """Update an Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    amenity_data = request.get_json(silent=True)
    if amenity_data is None:
        abort(400, "Not a JSON")

    amenity.update(**amenity_data)
    amenity.save()

    return jsonify(amenity.to_dict()), 200
