"""Test flight functionalities."""
# pylint: disable=no-member

from datetime import timedelta

import mock
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from api.mail import get_mail_notifications, send_mail_notifications
from factories import FlightFactory, UserFactory

from .models import Flight


# Create your tests here.
class TestFlightModel(TestCase):
    """Define test for flight model."""

    def test_flight_model_attr(self):
        """Test that all flight model attributes are accurate."""
        flight = FlightFactory()
        flight_obj = Flight.records.get(pk=flight.id)  # pylint: disable=no-member # noqa
        self.assertEqual(flight_obj.origin, flight.origin)
        self.assertEqual(flight_obj.destination, flight.destination)
        self.assertEqual(flight_obj.departure_date, flight.departure_date)
        self.assertEqual(flight_obj.plane_type, flight.plane_type)


class BaseTestClass(APITestCase):
    """Define base functionality for tests."""

    client = APIClient()
    User = get_user_model()
    data = {
        "origin": "lagos",
        "destination": "portharcourt",
        "departure_date": timezone.now().date() + timedelta(2),
        "plane_type": "business"
    }

    def setUp(self):
        """Define variables available to all test methods."""
        self.flights = [FlightFactory(), FlightFactory(), FlightFactory()]
        self.test_date = timezone.now().date() + timedelta(weeks=2)
        self.user = self.User.objects.create(username="james",
                                             password="testing",
                                             email="james@gmail.com")
        self.client.force_authenticate(user=self.user)


class TestFlightCreation(BaseTestClass):
    """Test flight creation functionalities."""

    def setUp(self):
        """Define custom setup for flight creation."""
        super().setUp()
        self.user.is_staff = True
        self.user.save()

    def test_fail_to_create_flight_when_unauthenticated(self):
        """User shouldn't be able to book flight when not authenticated."""
        self.client.force_authenticate(user=None)
        response = self.client.post(reverse("flight-list"), self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_only_admin_can_create_flights(self):
        """App should disallow non admins from creating flights."""
        self.user.is_staff = False
        self.user.save()
        response = self.client.post(reverse("flight-list"), self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(str(response.data["detail"]),
                         "You do not have permission to perform this action.")

    def test_creating_flight_as_admin(self):
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


class TestFetchingFlight(BaseTestClass):
    """Test fetching flight functionalities."""

    def test_retrieving_flights(self):
        """Test that user can retrieve flight reservations."""
        flight_a = self.flights[0]

        response = self.client.get(reverse("flight-list"))
        flight_res = Flight.records.first()
        self.assertEqual(flight_res.id, flight_a.id)  # pylint: disable=no-member # noqa
        self.assertEqual(flight_res.departure_date, flight_a.departure_date)
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


class TestMailMessaging(TestCase):
    """Define tests for flight mail notifications."""

    def generate_flight_and_passengers_for_test(self):
        """Prepare flight and user objects for mail test."""
        tomorrow = timezone.now().date() + timedelta(days=1)
        flights = [
            FlightFactory(departure_date=tomorrow),
            FlightFactory(departure_date=tomorrow)
        ]
        users = [UserFactory(), UserFactory()]
        # Add user 1 to flight 1
        flights[0].passengers.add(users[0])
        flights[0].save()

        # Add user 2 to flight 2
        flights[1].passengers.add(users[1])
        flights[1].save()
        return users

    def test_no_message_is_formed_when_there_is_no_flight_available(self):
        """App shouldn't generate messages when there are no scheduled flight."""  # noqa
        emails = get_mail_notifications()
        self.assertTrue(isinstance(emails, list))
        self.assertEqual(len(emails), 0)

    @mock.patch("api.mail.mail.get_connection")
    def test_send_mail_notification_not_called_when_no_mail_to_send(
            self, get_connection):
        """App shouldn't attempt to send mail when there is none."""
        # Call send_mail_notification when no flight has been booked
        con = get_connection()
        con.send_messages = mock.MagicMock()
        send_mail_notifications()
        self.assertFalse(con.send_messages.called)

    def test_generate_mail_messages_for_due_flight_passengers(self):
        """App should generate mail messages for passengers' flight notice."""
        users = self.generate_flight_and_passengers_for_test()
        emails = get_mail_notifications()
        self.assertTrue(isinstance(emails, list))
        self.assertEqual(len(emails), len(users))

    @mock.patch("api.mail.mail.get_connection")
    def test_send_mail_notification_called_on_sending_fligh_mail_notification(
            self, get_connection):
        """App should send mail notification to passengers.

        passengers whose flight date is about one day more should receive
        mail notification. Thus the app should call the send_messages() when
        triggered.

        """
        self.generate_flight_and_passengers_for_test()
        # Call send_mail_notification after flights have been booked
        con = get_connection()
        con.send_messages = mock.MagicMock()
        send_mail_notifications()
        self.assertTrue(con.send_messages.called)
