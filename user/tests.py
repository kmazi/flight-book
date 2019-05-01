from django.test import TestCase
from factories import FlightFactory


# Create your tests here.
class TestUserModel(TestCase):
    pass


class TestFlightModel(TestCase):
    def test_flight_model_attr(self):
        flight = FlightFactory()
        self.assertIsNotNone(flight.name)
        self.assertIsNotNone(flight.origin)
        self.assertIsNotNone(flight.destination)
        self.assertIsNotNone(flight.number)
        self.assertIsNotNone(flight.departure_date)
        self.assertIsNotNone(flight.departure_time)
