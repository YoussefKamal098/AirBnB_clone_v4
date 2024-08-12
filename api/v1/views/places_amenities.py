#!/usr/bin/python3
"""
This module defines the routes for the Place-Amenity relationship endpoint
in the HBNB API v1. It uses the Flask blueprint feature to define the routes,
The routes allow for the retrieval of a list of all Amenity objects in a
Place object, the deletion of an Amenity object from a Place object,
and the linking of an Amenity object to a Place object.
The module depends on the storage module from the models/engine package and
the Amenity and Place classes from the models package.
"""
from flask import jsonify, abort

from models.amenity import Amenity
from models.place import Place

from models import storage
from api.v1.views import app_views


@app_views.route("/places/<place_id>/amenities", methods=["GET"])
def get_place_amenities(place_id):
    """
    Get a list of all Amenity objects in a Place object with
    a given id  and return it in JSON format

    Returns a JSON-formatted list of Amenity objects in the Place object
    with the given id or 404 if no Place object with the given id is found
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    return jsonify([
        amenity.to_dict()
        for amenity in place.amenities
    ])


@app_views.route(
    "/places/<place_id>/amenities/<amenity_id>", methods=["DELETE"]
)
def delete_place_amenity(place_id, amenity_id):
    """
    Delete an Amenity object from a Place object with a given id

    Returns an empty dictionary with a status code of 200 if the Amenity
    object was successfully deleted, or 404 if the Place object with the
    given id or the Amenity object with the given id was not found
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if amenity not in place.amenities:
        abort(404)

    amenity.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["POST"])
def post_place_amenity(place_id, amenity_id):
    """
    Link an Amenity object to a Place object with a given id

    Returns a 201 status code and JSON-formatted dictionary of the Amenity
    object with the given id if the Amenity object was successfully linked
    to the Place object with the given id, or 404 if the Place object with
    the given id or the Amenity object with the given id was not found
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200

    place.amenities.append(amenity)
    storage.save()

    return jsonify(amenity.to_dict()), 201
