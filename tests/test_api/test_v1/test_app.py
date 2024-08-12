#!/usr/bin/python3
"""
test api/v1/app.py module that sets up and runs a
Flask application for the HBNB API
"""

import unittest
import flask

from api.v1.app import app


class AppTestCase(unittest.TestCase):
    """test app module"""

    def test_create_app(self):
        """check app instance with blueprint is created"""
        with app.test_client() as client:
            self.assertIsInstance(client, flask.testing.FlaskClient)


if __name__ == '__main__':
    unittest.main()
