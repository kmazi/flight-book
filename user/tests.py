"""Module containing tests for User and auth requests."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase


class BaseTest(TestCase):
    """Define common variables used in tests."""
    User = get_user_model()
    client = APIClient()

    def setUp(self):
        """Run before every test case."""
        self.user_attr = {
            "username": "gbengs",
            "password": "testing1",
            "first_name": "Gbenga",
            "last_name": "Oye",
            "email": "gbengs@gmail.com"
        }


# Create your tests here.
class TestUserModel(BaseTest):
    """Test the attributes of a user"""

    def test_creating_user_with_necessary_attributes(self):
        """Test user object creation"""

        user = self.User.objects.create(**self.user_attr)

        self.assertEqual(user.username, self.user_attr["username"])
        self.assertEqual(user.email, self.user_attr["email"])
        self.assertEqual(user.first_name, self.user_attr["first_name"])
        self.assertEqual(user.last_name, self.user_attr["last_name"])
        self.assertNotEqual(user.password, self.user_attr["password"])


class TestUserRegistration(APITestCase, BaseTest):
    """Test user registration functionalities"""

    def test_registering_user_with_valid_data(self):
        """Show that user with valid data can successfully register."""
        response = self.client.post(reverse("user-list"), self.user_attr)

        new_user = self.User.objects.get(username=self.user_attr["username"])
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["username"], new_user.username)
        self.assertIsNone(response.data.get("password"))
        self.assertEqual(response.data["first_name"], new_user.first_name)
        self.assertEqual(response.data["last_name"], new_user.last_name)
        self.assertEqual(response.data["email"], new_user.email)

    def test_registering_user_with_no_email(self):
        """App should fail to create a user with no email."""
        self.user_attr.pop("email")
        response = self.client.post(reverse("user-list"), self.user_attr)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["email"][0], "This field is required.")

    def test_registering_user_with_invalid_email(self):
        """App should fail to create a user with invalid email."""
        self.user_attr["email"] = "strangae@.com"
        response = self.client.post(reverse("user-list"), self.user_attr)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestUserLogin(APITestCase, BaseTest):
    """Test user login functionalities."""

    def setUp(self):
        """Setup variables for tests."""
        super().setUp()
        self.user = self.User.objects.create(**self.user_attr)

    def test_login_user_with_valid_username_and_password(self):
        """App should return access token when user successfully logs in."""
        data = {
            "username": self.user.username,
            "password": self.user_attr["password"]
        }
        response = self.client.post(reverse("login-list"), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], self.user.id)
        self.assertEqual(response.data["username"], self.user.username)
        self.assertIsNotNone(response.data["access"])
        self.assertIsNotNone(response.data["refresh"])

    def test_login_fails_when_username_is_invalid(self):
        """App should return 404 when signing in with invalid credentials."""
        data = {"username": "404", "password": self.user_attr["password"]}
        response = self.client.post(reverse("login-list"), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_login_fails_when_password_is_invalid(self):
        """Auth should fail when password is invalid."""
        data = {"username": self.user.username, "password": "wrongpassword"}
        response = self.client.post(reverse("login-list"), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_login_fails_when_no_username_in_form_is_sent(self):
        """Auth should fail when either username or password is missing."""
        data = {"password": self.user_attr["password"]}
        response = self.client.post(reverse("login-list"), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



username = "gbengs", password = "testing1", first_name = "Gbenga", last_name = "Oye", email = "gbengs@gmail.com"