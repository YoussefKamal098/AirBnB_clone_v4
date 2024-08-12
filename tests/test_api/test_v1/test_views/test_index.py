#!/usr/bin/python3
"""testing the index.py file"""

from os import getenv
import json
import unittest
from api.v1.app import app


storage = getenv("HBNB_TYPE_STORAGE")


class TestIndex(unittest.TestCase):
    """testing the index.py file"""
    def test_status(self):
        """test status function"""
        with app.test_client() as client:
            res = client.get('/api/v1/status')
            data = json.loads(res.data.decode('utf-8'))
            self.assertEqual(data, {'status': 'OK'})

    def test_count(self):
        """test count"""
        with app.test_client() as c:
            res = c.get('/api/v1/stats')
            data = json.loads(res.data.decode('utf-8'))

            for key, val in data.items():
                self.assertIsInstance(val, int)
                self.assertTrue(val >= 0)

    def test_404_not_found(self):
        """test for 404 error"""
        with app.test_client() as client:
            res = client.get('/api/v1/invalid')
            data = json.loads(res.data.decode('utf-8'))

            self.assertEqual(data, {"error": "Not found"})


if __name__ == '__main__':
    unittest.main()
