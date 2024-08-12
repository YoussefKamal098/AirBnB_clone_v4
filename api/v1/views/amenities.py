#!/usr/bin/python3
"""
This module sets up a Flask route to return a JSON list of all Amenity objects.
It also allows for GET, POST, PUT, and DELETE requests.

- GET requests return a JSON representation of an Amenity object
    or a 404 error if the Amenity object does not exist.

- POST requests create a new Amenity object.
    it returns a 400 error if the request is not JSON formatted or
    if the JSON body is missing a name key.

- PUT requests update an Amenity object.
    it returns a 404 error if the Amenity object does not exist
    or if the request is not JSON formatted.

- DELETE requests delete an Amenity object. it returns a 404 error if
    the Amenity object does not exist.

All responses are JSON formatted.

The following routes are defined:
GET /amenities GET /amenities/<amenity_id>
DELETE /amenities/<amenity_id>
POST /amenities PUT /amenities/

The following error codes are returned:
404: Not found
400: Not a JSON
400: Missing name
200: OK
201: Created
"""
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route("/amenities", methods=["GET"])
def get_amenities():
    """Return a JSON list of all Amenity objects"""
    return jsonify([
        amenity.to_dict()
        for amenity in storage.all(Amenity).values()
    ])


@app_views.route("/amenities/<amenity_id>", methods=["GET"])
def get_amenity(amenity_id):
    """Return a JSON representation of an Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"])
def delete_amenity(amenity_id):
    """Delete an Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    amenity.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route("/amenities/", methods=["POST"])
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
