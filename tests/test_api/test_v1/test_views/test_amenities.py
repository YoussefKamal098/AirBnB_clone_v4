#!/usr/bin/python3
"""testing the index route"""
import json
import unittest
from models.amenity import Amenity
from models import storage
from api.v1.app import app


class TestAmenities(unittest.TestCase):
    """test amenity"""
    def test_lists_amenities(self):
        """test amenity GET route"""
        with app.test_client() as client:
            res = client.get('/api/v1/amenities')
            self.assertEqual(res.status_code, 200)

            res = client.get('/api/v1/amenities/')
            self.assertEqual(res.status_code, 200)

    def test_create_amenity(self):
        """test amenity POST route"""
        with app.test_client() as client:
            res = client.post(
                '/api/v1/amenities/',
                data=json.dumps({"name": "Wifi"}),
                content_type="application/json"
            )

            self.assertEqual(res.status_code, 201)

    def test_delete_amenity(self):
        """test amenity DELETE route"""
        with app.test_client() as client:
            new_amenity = Amenity(name="Air conditioning")
            storage.new(new_amenity)
            res = client.get('api/v1/amenities/{}'.format(new_amenity.id))
            self.assertEqual(res.status_code, 200)

            resp = client.delete('api/v1/amenities/{}'.format(new_amenity.id))
            self.assertEqual(resp.status_code, 404)

            resp = client.get('api/v1/amenities/{}'.format(new_amenity.id))
            self.assertEqual(resp.status_code, 404)

    def test_get_amenity(self):
        """test amenity GET by id route"""
        with app.test_client() as client:
            new_amenity = Amenity(name="TV")
            storage.new(new_amenity)

            res = client.get('api/v1/amenities/{}'.format(new_amenity.id))
            self.assertEqual(res.status_code, 200)

    def test_update_amenity(self):
        """test amenity PUT route"""
        with app.test_client() as client:
            new_amenity = Amenity(name="Heating")
            storage.new(new_amenity)
            res = client.put(
                'api/v1/amenities/{}'.format(new_amenity.id),
                data=json.dumps({"name": "Kitchen"}),
                content_type="application/json"
            )

            self.assertEqual(res.status_code, 200)


if __name__ == '__main__':
    unittest.main()
