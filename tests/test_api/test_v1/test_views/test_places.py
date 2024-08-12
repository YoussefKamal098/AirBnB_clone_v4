#!/usr/bin/python3
"""testing the index route"""
import json
import unittest
from models.place import Place
from models.city import City
from models.state import State
from models.user import User
from models import storage
from api.v1.app import app


class TestPlaces(unittest.TestCase):
    """test city"""
    def test_lists_places_of_city(self):
        """test places GET route"""
        with app.test_client() as client:
            new_state = State(name="Russia")
            storage.new(new_state)
            new_city = City(name="Moscow", state_id=new_state.id)
            storage.new(new_city)

            new_user = User(email="example@123.com", password="0000")
            storage.new(new_user)

            new_place = Place(
                name="Becky's Bathhouse",
                description="best bath ever", number_rooms=4,
                number_bathrooms=1, max_guest=3,
                price_by_night=100, latitude=33.0,
                longitude=22.1, city_id=new_city.id,
                user_id=new_user.id
            )

            storage.new(new_place)

            resp = client.get('/api/v1/cities/{}/places'.format(new_city.id))
            self.assertEqual(resp.status_code, 200)

            # resp =client.get('/api/v1/cities/{}/places/'.format(new_city.id))
            # self.assertEqual(resp.status_code, 200)

    def test_create_place(self):
        """test place POST route"""
        with app.test_client() as client:
            new_state = State(name="China")
            storage.new(new_state)

            new_city = City(name="Chongqing", state_id=new_state.id)
            storage.new(new_city)

            new_user = User(email="example@123.com", password="0000")
            storage.new(new_user)

            resp = client.post(
                '/api/v1/cities/{}/places'.format(new_city.id),
                data=json.dumps(dict(
                    name="Becky's Bakery",
                    description="des",
                    number_rooms=4,
                    number_bathrooms=1, max_guest=3,
                    price_by_night=100,
                    latitude=33.0, longitude=22.1,
                    user_id=new_user.id)
                ), content_type="application/json"
            )

            self.assertEqual(resp.status_code, 201)

    def test_delete_place(self):
        """test place DELETE route"""
        with app.test_client() as client:
            new_state = State(name="USA")
            storage.new(new_state)

            new_city = City(name="New York", state_id=new_state.id)
            storage.new(new_city)

            new_user = User(email="example@123.com", password="0000")
            storage.new(new_user)

            new_place = Place(
                name="Becky's Bathhouse",
                description="des", number_rooms=4,
                number_bathrooms=1, max_guest=3,
                price_by_night=100, latitude=33.0,
                longitude=22.1, city_id=new_city.id,
                user_id=new_user.id
            )

            storage.new(new_place)

            resp = client.get('api/v1/places/{}'.format(new_place.id))
            self.assertEqual(resp.status_code, 200)

            resp = client.delete('api/v1/places/{}'.format(new_place.id))
            self.assertEqual(resp.status_code, 404)

            resp = client.get('api/v1/places/{}'.format(new_place.id))
            self.assertEqual(resp.status_code, 404)

    def test_get_place(self):
        """test place GET by id route"""
        with app.test_client() as client:
            new_state = State(name="Poland")
            storage.new(new_state)

            new_city = City(name="Warsaw", state_id=new_state.id)
            storage.new(new_city)

            new_user = User(email="abc@123.com", password="chicken")
            storage.new(new_user)

            new_place = Place(
                name="Becky's Bathhouse",
                description="best bath ever", number_rooms=3,
                number_bathrooms=0, max_guest=2,
                price_by_night=100, latitude=33.0,
                longitude=22.1, city_id=new_city.id,
                user_id=new_user.id
            )

            storage.new(new_place)

            res = client.get('/api/v1/places/{}'.format(new_place.id))
            self.assertEqual(res.status_code, 200)

    def test_update_place(self):
        """test place PUT route"""
        with app.test_client() as client:
            new_state = State(name="Beckystan")
            storage.new(new_state)

            new_city = City(name="Chensville", state_id=new_state.id)
            storage.new(new_city)

            new_user = User(email="example@123.com", password="00000")
            storage.new(new_user)

            new_place = Place(
                name="Becky's Bathhouse",
                description="des", number_rooms=4,
                number_bathrooms=1, max_guest=3,
                price_by_night=100, latitude=33.0,
                longitude=22.1, city_id=new_city.id,
                user_id=new_user.id
            )

            storage.new(new_place)

            resp = client.put(
                'api/v1/places/{}'.format(new_place.id),
                data=json.dumps({"name": "Becky's Billards"}),
                content_type="application/json"
            )

            self.assertEqual(resp.status_code, 200)


if __name__ == '__main__':
    unittest.main()
