#!/usr/bin/python3
"""
This module sets up a Flask route to return a JSON list of all Place objects.
It also allows for GET, POST, PUT, and DELETE requests. and it also searches
for Place objects by state, city, and amenity linked to the Place.
"""
from flask import jsonify, abort, request

from models.user import User
from models.city import City
from models.place import Place
from models import storage

from api.v1.views import app_views


@app_views.route("/cities/<city_id>/places", methods=["GET"])
def get_places(city_id):
    """
    Return a JSON list of all Place objects in a City object with city_id.
    or 404 error if city_id is not linked to any City object.

    Return 200 status code with the list of Place objects
    with City with <city_id> in JSON format if success.
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    return jsonify([
        place.to_dict()
        for place in city.places
    ])


@app_views.route("/places/<place_id>", methods=["GET"])
def get_place(place_id):
    """
    Return a JSON representation of a Place object
    or 404 error if not found.

    Return 200 status code with the Place object in JSON format if success.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"])
def delete_place(place_id):
    """
    Delete a Place object with place_id or 404 error if not found.

    Return 200 status code with an empty JSON object if success.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    place.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=["POST"])
def post_place(city_id):
    """
    Create a new Place object in a City object with city_id.

    Return 404 if city_id is not linked to any City object,
    or 400 error if not a JSON, missing user_id or missing name.

    Return 201 status code with the new Place object in JSON format if success.
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    place_data = request.get_json(silent=True)
    if not place_data:
        abort(400, "Not a JSON")
    if "user_id" not in place_data:
        abort(400, "Missing user_id")
    if "name" not in place_data:
        abort(400, "Missing name")

    user = storage.get(User, place_data.get("user_id"))
    if not user:
        abort(404)

    new_place = Place(city_id=city_id, **place_data)
    new_place.save()

    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"])
def put_place(place_id):
    """
    Update a Place object with place_id. Return 404 if not found.
    Return 400 if not a JSON.

    Return 200 with the updated Place object in JSON format if success.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    place_data = request.get_json(silent=True)
    if place_data is None:
        abort(400, "Not a JSON")

    place.update(**place_data)
    place.save()

    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'])
def places_search():
    """
    Search for Place objects based on the JSON in the request.
    Return 400 if not a JSON.

    It filters the Place objects by state, city,
    and amenity linked to the Place.

    The JSON should have the following keys:
    - states: list of state ids to filter by (OR logic) (empty list means all)
    - cities: list of city ids to filter by (OR logic) (empty list means all)
    - amenities: list of amenity ids to filter by \
        (AND logic) (empty list means all)

    If the JSON is empty, return all Place objects.

    Return 200 with a list of Place objects in JSON format if success.
    """
    # Get search data as JSON
    # (Return 400 (Bad Request) if not JSON data is provided)
    search_data = request.get_json(silent=True)
    if search_data is None:
        abort(400, "Not a JSON")

    # Fetch all places
    places = storage.all(Place).values()

    # List to store filtered places
    filtered_places = []

    # Iterate through all places
    for place in places:
        # Initialize variables to track filter matches (default True)
        state_matches = True
        city_matches = True

        # Check for state filter
        if search_data.get("states"):
            # Check if place's city state matches any in search data
            state_matches = place.city.state_id in search_data["states"]

            # If state filter matches, set city_matches to False (OR logic)
            city_matches = False

        # Check for city filter (only if no state filter or \
        # "cities" key exists)
        if ((not state_matches or not search_data.get("states")) and
                search_data.get("cities")):
            # Check if place's city ID matches any in search data
            city_matches = place.city_id in search_data["cities"]

            # If city filter matches, set state_matches to False (OR logic)
            state_matches = False

        # Check for amenity filter
        amenity_matches = True
        if search_data.get("amenities"):
            # Check if all amenity IDs in search data are present \
            # in the place's amenities
            amenity_matches = all(
                amenity_id in [amenity.id for amenity in place.amenities]
                for amenity_id in search_data["amenities"]
            )

        # Add place to filtered list if state or \
        # city matches AND all amenity matches
        if (state_matches or city_matches) and amenity_matches:
            filtered_places.append(place)

    # Return JSON response with list of place dictionaries
    return jsonify([place.to_dict() for place in filtered_places])
