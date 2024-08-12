#!/usr/bin/python3
"""testing the cities routes"""
import json
import unittest
from models.state import State
from models.city import City
from models import storage
from api.v1.app import app


class TestCities(unittest.TestCase):
    """test cities.py file for cities routes"""
    def test_lists_cities_of_state(self):
        """test cities GET route"""
        with app.test_client() as client:
            new_state = State(name="Egy")
            storage.new(new_state)

            new_city = City(name="Cairo", state_id=new_state.id)
            storage.new(new_city)

            res = client.get('/api/v1/states/{}/cities'.format(new_state.id))
            self.assertEqual(res.status_code, 200)

            # res =client.get('/api/v1/states/{}/cities/'.format(new_state.id))
            # self.assertEqual(res.status_code, 200)

    def test_create_city(self):
        """test city POST route"""
        with app.test_client() as client:
            new_state = State(name="China")
            storage.new(new_state)

            new_city = City(name="Chongqing", state_id=new_state.id)
            storage.new(new_city)

            resp = client.post(
                '/api/v1/states/{}/cities'.format(new_state.id),
                data=json.dumps({"name": "Guangzhou"}),
                content_type="application/json"
            )

            self.assertEqual(resp.status_code, 201)

    def test_delete_city(self):
        """test city DELETE route"""
        with app.test_client() as client:
            new_state = State(name="Russia")
            storage.new(new_state)

            new_city = City(name="Moscow", state_id=new_state.id)
            storage.new(new_city)

            resp = client.get('api/v1/cities/{}'.format(new_city.id))
            self.assertEqual(resp.status_code, 200)

            resp = client.delete('api/v1/cities/{}'.format(new_city.id))
            self.assertEqual(resp.status_code, 404)

            resp = client.get('api/v1/cities/{}'.format(new_city.id))
            self.assertEqual(resp.status_code, 404)

    def test_get_city(self):
        """test city GET by id route"""
        with app.test_client() as client:
            new_state = State(name="India")
            storage.new(new_state)

            new_city = City(name="Mumbai", state_id=new_state.id)
            storage.new(new_city)

            resp = client.get('/api/v1/states/{}/cities'.format(new_state.id))
            self.assertEqual(resp.status_code, 200)

    def test_update_city(self):
        """test city PUT route"""
        with app.test_client() as client:
            new_state = State(name="USA")
            storage.new(new_state)

            new_city = City(name="New York", state_id=new_state.id)
            storage.new(new_city)

            resp = client.put(
                'api/v1/cities/{}'.format(new_city.id),
                data=json.dumps({"name": "San Francisco"}),
                content_type="application/json"
            )

            self.assertEqual(resp.status_code, 200)


if __name__ == '__main__':
    unittest.main()
