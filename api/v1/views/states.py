#!/usr/bin/python3
"""
This module sets up a Flask route to return a JSON list of all State objects.
It also allows for GET, POST, PUT, and DELETE requests.

- GET requests return a JSON representation of a State object or
    a 404 error if the State object does not exist.

- POST requests create a new State object. returns a 400 error if the request
    is not JSON formatted or if the JSON body is missing a name key.

- PUT requests update a State object. returns a 404 error if the
    State object does not exist or if the request is not JSON formatted.


- DELETE requests delete a State object. returns a 404 error
    if the State object does not exist.

All responses are JSON formatted.

The following routes are defined:
GET /states
GET /states/<state_id>
DELETE /states/<state_id>
POST /states
PUT /states/

The following error codes are returned:
404: Not found
400: Not a JSON
400: Missing name
200: OK
201: Created
"""

from flask import jsonify, abort, request

from models import storage
from models.state import State

from api.v1.views import app_views


@app_views.route("/states/", methods=["GET"])
def get_states():
    """Return a JSON list of all State objects"""
    return jsonify([
        state.to_dict()
        for state in storage.all(State).values()
    ])


@app_views.route("/states/<state_id>", methods=["GET"])
def get_state(state_id):
    """Return a JSON representation of a State object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"])
def delete_state(state_id):
    """Delete a State object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    state.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route("/states/", methods=["POST"])
def post_state():
    """Create a new State object"""
    state_data = request.get_json(silent=True)

    if not state_data:
        abort(400, "Not a JSON")
    if "name" not in state_data:
        abort(400, "Missing name")

    new_state = State(name=state_data.get("name"))
    new_state.save()

    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"])
def put_state(state_id):
    """Update a State object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    update_data = request.get_json(silent=True)
    if not update_data:
        abort(400, "Not a JSON")

    state.update(**update_data)
    state.save()

    return jsonify(state.to_dict()), 200
