#!/usr/bin/python3
"""
This module sets up a Flask route to return a JSON list of all State objects.
It also allows for GET, POST, PUT, and DELETE requests.
"""

from flask import jsonify, abort, request
from flasgger import swag_from

from models import storage
from models.state import State


from api.v1.views import app_views


@app_views.route("/states/", methods=["GET"])
@swag_from('documentation/state/all_states.yml')
def get_states():
    """Return a JSON list of all State objects"""
    return jsonify([
        state.to_dict()
        for state in storage.all(State).values()
    ])


@app_views.route("/states/<state_id>", methods=["GET"])
@swag_from('documentation/state/get_state.yml')
def get_state(state_id):
    """Return a JSON representation of a State object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"])
@swag_from('documentation/state/delete_state.yml')
def delete_state(state_id):
    """Delete a State object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    state.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route("/states/", methods=["POST"])
@swag_from('documentation/state/post_state.yml')
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
@swag_from('documentation/state/put_state.yml')
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
