#!/usr/bin/python3
"""testing the users routes"""
import json
import unittest
from models.user import User
from models import storage
from api.v1.app import app


class TestUsers(unittest.TestCase):
    """test user"""
    def test_lists_users(self):
        """test user GET route"""
        with app.test_client() as client:
            res = client.get('/api/v1/users')
            self.assertEqual(res.status_code, 200)

            res = client.get('/api/v1/users/')
            self.assertEqual(res.status_code, 200)

    def test_create_user(self):
        """test user POST route"""
        with app.test_client() as client:
            res = client.post(
                '/api/v1/users/',
                data=json.dumps({"email": "123@abc.com", "password": "0000"}),
                content_type="application/json")

            self.assertEqual(res.status_code, 201)

    def test_delete_user(self):
        """test user DELETE route"""
        with app.test_client() as client:
            new_user = User(
                first_name="Jacob", last_name="Joe",
                email="example@abc.com", password="00000"
            )

            storage.new(new_user)

            res = client.get('api/v1/users/{}'.format(new_user.id))
            self.assertEqual(res.status_code, 200)

            res = client.delete('api/v1/users/{}'.format(new_user.id))
            self.assertEqual(res.status_code, 404)

            res = client.get('api/v1/users/{}'.format(new_user.id))
            self.assertEqual(res.status_code, 404)

    def test_get_user(self):
        """test user GET by id route"""
        with app.test_client() as client:
            new_user = User(
                first_name="Foo", last_name="Bar",
                email="example@abc.com", password="00000"
            )

            storage.new(new_user)

            res = client.get('api/v1/users/{}'.format(new_user.id))
            self.assertEqual(res.status_code, 200)

    def test_update_user(self):
        """test user PUT route"""
        with app.test_client() as client:
            new_user = User(
                first_name="foo", last_name="Bar",
                email="example@abc.com", password="00000"
            )

            storage.new(new_user)

            res = client.put(
                'api/v1/users/{}'.format(new_user.id),
                data=json.dumps({
                    "first_name": "Julia",
                    "last_name": "James"
                }), content_type="application/json"
            )

            self.assertEqual(res.status_code, 200)


if __name__ == '__main__':
    unittest.main()
