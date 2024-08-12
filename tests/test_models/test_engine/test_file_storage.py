#!/usr/bin/python3
"""test for File storage"""
import os
import unittest
from models import storage
from models.state import State

storage_type = os.getenv("HBNB_TYPE_STORAGE")


@unittest.skipIf(storage_type == 'db', 'File Storage test')
class TestFileStorage(unittest.TestCase):
    """Tests the File Storage"""
    def test_get(self):
        """Test if get method retrieves obj requested"""
        new_state = State(name="NewYork")
        storage.new(new_state)

        result = storage.get(State, new_state.id)

        self.assertTrue(result.id, new_state.id)
        self.assertIsInstance(result, State)

    def test_count(self):
        """Test if count method returns expected number of objects"""
        old_count = storage.count(State)

        new_state1 = State(name="NewYork")
        storage.new(new_state1)

        new_state2 = State(name="Virginia")
        storage.new(new_state2)

        new_state3 = State(name="California")
        storage.new(new_state3)

        self.assertEqual(old_count + 3, storage.count(State))


if __name__ == '__main__':
    unittest.main()
