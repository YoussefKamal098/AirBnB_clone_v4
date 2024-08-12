#!/usr/bin/python3
"""
This module initializes the Flask blueprint for the API views.
It imports all the views and sets the url prefix.
It also initializes the blueprint.
see each view for more information on the routes.
"""

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1/')


if app_views:
    from api.v1.views.index import *
    from api.v1.views.states import *
    from api.v1.views.cities import *
    from api.v1.views.amenities import *
    from api.v1.views.users import *
    from api.v1.views.places import *
    from api.v1.views.places_reviews import *
    from api.v1.views.places_amenities import *
