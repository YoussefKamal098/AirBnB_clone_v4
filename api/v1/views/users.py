#!/usr/bin/python3
"""
This module sets up a Flask route to return a JSON list of all User objects.
It also allows for GET, POST, PUT, and DELETE requests.
"""
from flask import jsonify, abort, request
from flasgger import swag_from
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route("/users", methods=["GET"])
@swag_from('documentation/user/all_users.yml')
def get_users():
    """Return a JSON list of all User objects"""
    return jsonify([
        user.to_dict()
        for user in storage.all(User).values()
    ])


@app_views.route("/users/<user_id>", methods=["GET"])
@swag_from('documentation/user/get_user.yml')
def get_user(user_id):
    """Return a JSON representation of a User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"])
@swag_from('documentation/user/delete_user.yml')
def delete_user(user_id):
    """Delete a User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    user.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route("/users/", methods=["POST"])
@swag_from('documentation/user/post_user.yml')
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
@swag_from('documentation/user/put_user.yml')
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
