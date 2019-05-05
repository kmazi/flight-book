from django.test import TestCase
from factories import FlightFactory
from .models import Flight


# Create your tests here.
class TestFlightModel(TestCase):
    def test_flight_model_attr(self):
        flight = FlightFactory()
        flight_obj = Flight.objects.get(pk=flight.id)
        self.assertIsNotNone(flight.name)
        self.assertEqual(flight_obj.name, flight.name)
        self.assertIsNotNone(flight.origin)
        self.assertEqual(flight_obj.origin, flight.origin)
        self.assertIsNotNone(flight.destination)
        self.assertEqual(flight_obj.destination, flight.destination)
        self.assertIsNotNone(flight.number)
        self.assertEqual(flight_obj.number, flight.number)
        self.assertIsNotNone(flight.departure_date)
        self.assertEqual(flight_obj.departure_date, flight.departure_date)
        self.assertIsNotNone(flight.departure_time)
        self.assertEqual(flight_obj.departure_time, flight.departure_time)
