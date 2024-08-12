#!/usr/bin/python3
"""
This module sets up a Flask route to return a JSON list of all User objects.
It also allows for GET, POST, PUT, and DELETE requests.

- GET requests return a JSON representation of a User object or
    a 404 error if the User object does not exist.

- POST requests create a new User object. returns a 400 error if the request is
    not JSON formatted or if the JSON body is missing an email or password key.

- PUT requests update a User object. returns a 404 error if the User
    object does not exist or if the request is not JSON formatted.

- DELETE requests delete a User object. returns a 404 error if
    the User object does not exist.

All responses are JSON formatted.

DELETE requests are expected to have an empty JSON body.

GET requests do not require a JSON body.

The following routes are defined:
GET /users
GET /users/<user_id>
DELETE /users/<user_id>
POST /users
PUT /users/<user_id>

The following error codes are returned:
404: Not found
400: Not a JSON
400: Missing email
400: Missing password
200: OK
201: Created
"""
from flask import jsonify, abort, request
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route("/users", methods=["GET"])
def get_users():
    """Return a JSON list of all User objects"""
    return jsonify([
        user.to_dict()
        for user in storage.all(User).values()
    ])


@app_views.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    """Return a JSON representation of a User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    """Delete a User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    user.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route("/users/", methods=["POST"])
def post_user():
    """Create a new User object"""
    user_data = request.get_json(silent=True)

    if not user_data:
        abort(400, "Not a JSON")
    if "email" not in user_data:
        abort(400, "Missing email")
    if "password" not in user_data:
        abort(400, "Missing password")

    new_user = User(**user_data)
    new_user.save()

    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"])
def put_user(user_id):
    """Update a User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    user_data = request.get_json(silent=True)
    if user_data is None:
        abort(400, "Not a JSON")

    user.update(**user_data)
    user.save()

    return jsonify(user.to_dict()), 200
