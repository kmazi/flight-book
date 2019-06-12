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
        self.assertIsNotNone(flight.origin)
        self.assertEqual(flight_obj.origin, flight.origin)
        self.assertIsNotNone(flight.destination)
        self.assertEqual(flight_obj.destination, flight.destination)
        self.assertIsNotNone(flight.departure_date)
        self.assertEqual(flight_obj.departure_date, flight.departure_date)
        self.assertIsNotNone(flight.return_date)
        self.assertEqual(flight_obj.return_date, flight.return_date)
        self.assertIsNotNone(flight_obj.plane_type)
        self.assertEqual(flight_obj.plane_type, flight.plane_type)


class TestFlightReservation(APITestCase):
    """Test flight reservation functionalities."""

    client = APIClient()

    def setUp(self):
        """Define variables available to all test methods."""
        self.flights = [FlightFactory(), FlightFactory(), FlightFactory()]

    def test_reserving_flight(self):
        """Test that user can reserve flight."""
        data = {
            "name": "Samuel Smith",
            "origin": "lagos",
            "destination": "portharcourt",
            "departure_date": dt.now().date() + timedelta(2),
            "return_date": dt.now().date() + timedelta(7),
            "plane_type": "business"
        }
        response = self.client.post(reverse("flight-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data["id"])
        self.assertEqual(response.data["origin"], data["origin"])
        self.assertEqual(response.data["destination"], data["destination"])
        self.assertEqual(response.data["departure_date"],
                         data["departure_date"].strftime("%Y-%m-%d"))
        self.assertEqual(response.data["return_date"],
                         data["return_date"].strftime("%Y-%m-%d"))

    def test_retrieving_reserved_flights(self):
        """Test that user can retrieve flight reservations."""
        flight_a = self.flights[0]

        response = self.client.get(reverse("flight-list"))
        flight_res = Flight.records.first()
        self.assertEqual(flight_res.departure_date, flight_a.departure_date)
        self.assertEqual(flight_res.return_date, flight_a.return_date)
        self.assertEqual(flight_res.origin, flight_a.origin)
        self.assertEqual(flight_res.destination, flight_a.destination)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(self.flights))

    def test_retrieving_reserved_flights_for_given_date(self):
        """Test that flights for a specific date can be retrieved."""
        date = dt.today().date() + timedelta(weeks=2)
        FlightFactory(departure_date=date)
        response = self.client.get(
            f"{reverse('flight-list')}?departure_date={date}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["departure_date"], date.isoformat())
