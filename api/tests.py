"""Test flight functionalities."""

from datetime import datetime as dt
from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from factories import FlightFactory

from .models import Flight


# Create your tests here.
class TestFlightModel(TestCase):
    """Define test for flight model."""

    def test_flight_model_attr(self):
        """Test that all flight model attributes are accurate."""
        flight = FlightFactory()
        flight_obj = Flight.records.get(pk=flight.id)
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


class TestFlightReservation(APITestCase):
    """Test flight reservation functionalities."""

    client = APIClient()

    def test_reserve_flight(self):
        """Test that user can reserve flight."""
        data = {
            "origin": "lagos",
            "destination": "portharcourt",
            "departure_date": dt.now() + timedelta(2),
            "return_date": dt.now() + timedelta(7),
            "plane_type": "business"
        }
        response = self.client.post(reverse("flight-list"), data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(response.data, data)
