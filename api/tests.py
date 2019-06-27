"""Test flight functionalities."""
# pylint: disable=no-member

from datetime import datetime, timedelta

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


class BaseTestClass(APITestCase):
    """Define base functionality for tests."""

    client = APIClient()
    User = get_user_model()
    data = {
        "origin": "lagos",
        "destination": "portharcourt",
        "departure_date": datetime.now().date() + timedelta(2),
        "return_date": datetime.now().date() + timedelta(7),
        "plane_type": "business"
    }

    def setUp(self):
        """Define variables available to all test methods."""
        self.flights = [FlightFactory(), FlightFactory(), FlightFactory()]
        self.test_date = datetime.today().date() + timedelta(weeks=2)
        self.user = self.User.objects.create(username="james",
                                             password="testing",
                                             email="james@gmail.com")
        self.client.force_authenticate(user=self.user)


class TestFlightCreation(BaseTestClass):
    """Test flight reservation functionalities."""

    def test_fail_to_create_flight_when_unauthenticated(self):
        """User shouldn't be able to book flight when not authenticated."""
        self.client.force_authenticate(user=None)
        response = self.client.post(reverse("flight-list"), self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_creating_flight(self):
        """Test that user can reserve flight."""
        response = self.client.post(reverse("flight-list"), self.data)
        booked_flight = Flight.records.get(
            destination=self.data["destination"])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data["id"])
        self.assertEqual(response.data["id"], booked_flight.id)
        self.assertEqual(response.data["origin"], self.data["origin"])
        self.assertEqual(response.data["plane_type"], self.data["plane_type"])
        self.assertEqual(response.data["destination"],
                         self.data["destination"])
        self.assertEqual(response.data["departure_date"],
                         self.data["departure_date"].strftime("%Y-%m-%d"))
        self.assertEqual(response.data["return_date"],
                         self.data["return_date"].strftime("%Y-%m-%d"))

    def test_retrieving_flights(self):
        """Test that user can retrieve flight reservations."""
        flight_a = self.flights[0]

        response = self.client.get(reverse("flight-list"))
        flight_res = Flight.records.first()
        self.assertEqual(flight_res.id, flight_a.id)  # pylint: disable=no-member # noqa
        self.assertEqual(flight_res.departure_date, flight_a.departure_date)
        self.assertEqual(flight_res.return_date, flight_a.return_date)
        self.assertEqual(flight_res.origin, flight_a.origin)
        self.assertEqual(flight_res.plane_type, flight_a.plane_type)
        self.assertEqual(flight_res.destination, flight_a.destination)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(self.flights))

    def test_retrieving_flights_for_given_date(self):
        """Test that flights for a specific date can be retrieved."""
        FlightFactory(departure_date=self.test_date)
        response = self.client.get(
            f"{reverse('flight-list')}?departure={self.test_date}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["departure_date"],
                         self.test_date.isoformat())

    def test_retrieving_flights_by_return_dates(self):
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


class TestFlightBooking(BaseTestClass):
    """Test functionality when booking flights."""

    def test_book_flight_successfully(self):
        """Users can book available flights with right credentials."""
        test_flight = Flight.records.first()
        response = self.client.patch(reverse('flight-book-flight',
                                             kwargs={"pk": test_flight.id}),
                                     data={"username": self.user.username})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], test_flight.id)
        self.assertEqual(response.data["origin"], test_flight.origin)
        self.assertEqual(response.data["destination"], test_flight.destination)
        self.assertEqual(response.data["departure_date"],
                         test_flight.departure_date.isoformat())
        self.assertEqual(response.data["plane_type"], test_flight.plane_type)
        self.assertEqual(len(test_flight.passengers.all()), 1)

    def test_fail_to_book_flight_for_unauthenticated_user(self):
        """Unauthenticated user shouldn't book flight successfully."""
        test_flight = Flight.records.first()
        self.client.force_authenticate(user=None)
        response = self.client.patch(reverse('flight-book-flight',
                                             kwargs={"pk": test_flight.id}),
                                     data={"username": self.user.username})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_fail_to_book_same_flight_more_than_once(self):
        """App should fail to book same flight for a user more than once."""
        test_flight = Flight.records.first()
        test_flight.passengers.add(self.user)
        response = self.client.patch(reverse('flight-book-flight',
                                             kwargs={"pk": test_flight.id}),
                                     data={"username": self.user.username})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data[0]),
                         "Flight has already been booked by you")
