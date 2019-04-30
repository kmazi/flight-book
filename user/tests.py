from django.test import TestCase
from factories import FlightFactory

# Create your tests here.
class TestUserModel(TestCase):
    pass


class TestFlightModel(TestCase):
    def test_flight_model_attr(self):
        flight = FlightFactory()
        assertIsNotNone(flight.name)
        assertIsNotNone(flight.origin)
        assertIsNotNone(flight.destination)
        assertIsNotNone(flight.number)
        assertIsNotNone(flight.departure_date)
        assertIsNotNone(flight.departure_time)