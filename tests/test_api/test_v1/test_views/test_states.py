#!/usr/bin/python3
"""testing the states routes"""
import json
import unittest
from models.state import State
from models import storage
from api.v1.app import app


class TestStates(unittest.TestCase):
    """test state.py file for states routes"""
    def test_lists_states(self):
        """test state GET route"""
        with app.test_client() as client:
            resp = client.get('/api/v1/states')
            self.assertEqual(resp.status_code, 200)

            resp = client.get('/api/v1/states/')
            self.assertEqual(resp.status_code, 200)

    def test_create_state(self):
        """test state POST route"""
        with app.test_client() as client:
            resp = client.post(
                '/api/v1/states/',
                data=json.dumps({"name": "China"}),
                content_type="application/json"
            )

            self.assertEqual(resp.status_code, 201)

    def test_delete_state(self):
        """test state DELETE route"""
        with app.test_client() as client:
            new_state = State(name="India")
            storage.new(new_state)

            resp = client.get('api/v1/states/{}'.format(new_state.id))
            self.assertEqual(resp.status_code, 200)

            resp = client.delete('api/v1/states/{}'.format(new_state.id))
            self.assertEqual(resp.status_code, 404)

            resp = client.get('api/v1/states/{}'.format(new_state.id))
            self.assertEqual(resp.status_code, 404)

    def test_get_state(self):
        """test state GET by id route"""
        with app.test_client() as client:
            new_state = State(name="Russia")
            storage.new(new_state)

            resp = client.get('api/v1/states/{}'.format(new_state.id))
            self.assertEqual(resp.status_code, 200)

    def test_update_state(self):
        """test state PUT route"""
        with app.test_client() as client:
            new_state = State(name="Canada")
            storage.new(new_state)

            resp = client.put(
                'api/v1/states/{}'.format(new_state.id),
                data=json.dumps({"name": "USA"}),
                content_type="application/json"
            )

            self.assertEqual(resp.status_code, 200)


if __name__ == '__main__':
    unittest.main()
