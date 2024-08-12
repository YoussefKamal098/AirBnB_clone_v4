#!/usr/bin/python3
"""
Module Overview

This module defines the Flask routes and views for handling RESTful API actions
related to the `Review` class. It supports the following HTTP methods: `GET`,
`POST`, `PUT`, and `DELETE`. The routes return JSON-formatted responses and
interact with the `Review` objects stored in the application's
data storage system.

Functionality

- RESTful API Actions: This module implements the default RESTful actions for
  the `Review` class, including creating, retrieving, updating, and deleting
  `Review` objects.

- Response Codes: The module returns standard HTTP status codes:
  - `200 OK`: Returned when a `Review` object is successfully retrieved,
    deleted, or updated.
  - `201 Created`: Returned when a new `Review` object is successfully created.
  - `400 Bad Request`: Returned when a request contains invalid JSON or when a
    required attribute is missing.
  - `404 Not Found`: Returned when a `Review` object is not found.

- Integration: This module is integrated with the API blueprint in the
  `__init__.py` file and interacts with the `Review` class from the `models`
  module. It utilizes the `storage` object to interface with
  the underlying file storage or database engine.

- Data Handling: All responses are returned in JSON format,
  ensuring consistency with the application's API design.

Module Connections

- API Blueprint: The routes defined in this module are connected to the API
  blueprint initialized in the `__init__.py` file.

- Models Module: This module is directly connected to the `Review` class within
  the `models` module, leveraging the `storage` object
  to perform data operations.

- Related Entities: While primarily focused on the `Review` class, this module
  also supports operations related to `Place` and `User` objects,
  as part of the main Flask application's broader functionality.
"""

from flask import jsonify, request, abort

from models.place import Place
from models.review import Review
from models.user import User
from models import storage

from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def get_reviews(place_id):
    """
    Retrieves the list of all Review objects of a Place.

    Returns a JSON list of all Review objects of a Place
    or a 404 error if the Place is not found.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    """
    Retrieves a Review object.

    Returns a JSON representation of a Review object
    or a 404 error if the Review is not found.
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """
    Deletes a Review object.

    Returns an empty dictionary with the status code 200
    or a 404 error if the Review is not found.
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    storage.delete(review)
    storage.save()

    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """
    Creates a new Review object.

    Creates a Review object linked to a Place based on the JSON
    received in the request.

    Returns the new Review with the status code 201
    or a 400 error if the JSON is not valid or user_id or text is missing
    or a 404 error if the Place is not found.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')

    if 'user_id' not in data:
        abort(400, 'Missing user_id')

    user_id = data['user_id']
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    if 'text' not in data:
        abort(400, 'Missing text')

    review = Review(place_id=place_id, **data)
    review.save()

    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """
    Updates a Review object.

    Updates a Review object based on the JSON received in the request.

    Returns the updated Review with the status code 200
    or a 400 error if the JSON is not valid
    or a 404 error if the Review is not found.
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')

    review.update(**data)
    review.save()

    return jsonify(review.to_dict()), 200
