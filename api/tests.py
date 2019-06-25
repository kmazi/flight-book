"""Test flight functionalities."""
# pylint: disable=no-member


from datetime import datetime as dt
from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
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
        flight_obj = Flight.records.get(pk=flight.id)  # pylint: disable=no-member # noqa
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
    User = get_user_model()
    data = {
        "origin": "lagos",
        "destination": "portharcourt",
        "departure_date": dt.now().date() + timedelta(2),
        "return_date": dt.now().date() + timedelta(7),
        "plane_type": "business"
    }

    def setUp(self):
        """Define variables available to all test methods."""
        self.flights = [FlightFactory(), FlightFactory(), FlightFactory()]
        self.test_date = dt.today().date() + timedelta(weeks=2)
        self.user = self.User.objects.create(username="james",
                                             password="testing",
                                             email="james@gmail.com")
        self.client.force_authenticate(user=self.user)

    def test_fail_to_book_flight_when_unauthenticated(self):
        """User shouldn't be able to book flight when not authenticated."""
        self.client.force_authenticate(user=None)
        response = self.client.post(reverse("flight-list"), self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @pytest.mark.one
    def test_reserving_flight(self):
        """Test that user can reserve flight."""
        response = self.client.post(reverse("flight-list"), self.data)
        booked_flight = Flight.records.get(
            destination=self.data["destination"])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data["id"])
        self.assertEqual(response.data["id"], booked_flight.id)
        self.assertEqual(response.data["origin"], self.data["origin"])
        self.assertEqual(response.data["destination"],
                         self.data["destination"])
        self.assertEqual(response.data["departure_date"],
                         self.data["departure_date"].strftime("%Y-%m-%d"))
        self.assertEqual(response.data["return_date"],
                         self.data["return_date"].strftime("%Y-%m-%d"))

    def test_retrieving_reserved_flights(self):
        """Test that user can retrieve flight reservations."""
        flight_a = self.flights[0]

        response = self.client.get(reverse("flight-list"))
        flight_res = Flight.records.first()
        self.assertEqual(flight_res.id, flight_a.id)  # pylint: disable=no-member # noqa
        self.assertEqual(flight_res.departure_date, flight_a.departure_date)
        self.assertEqual(flight_res.return_date, flight_a.return_date)
        self.assertEqual(flight_res.origin, flight_a.origin)
        self.assertEqual(flight_res.destination, flight_a.destination)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(self.flights))

    def test_retrieving_reserved_flights_for_given_date(self):
        """Test that flights for a specific date can be retrieved."""
        FlightFactory(departure_date=self.test_date)
        response = self.client.get(
            f"{reverse('flight-list')}?departure={self.test_date}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["departure_date"],
                         self.test_date.isoformat())

    def test_retrieving_reserved_flights_by_return_dates(self):
        """Test retrieving return flights scheduled for a specific days."""
        FlightFactory(return_date=self.test_date)
        response = self.client.get(
            f"{reverse('flight-list')}?return_date={self.test_date}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["return_date"],
                         self.test_date.isoformat())

    def test_retrieve_flights_by_both_return_and_departure_dates(self):
        """Test querying flights by both return and departure date."""
        FlightFactory(return_date=self.test_date)
        base_url = reverse("flight-list")
        response = self.client.get(
            "{}?return_date={}&departure_date={}".format(
                base_url, self.test_date, self.flights[0].departure_date))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
