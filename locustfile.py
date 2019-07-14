"""Define load testing for application."""

import os
from datetime import datetime, timedelta

from locust import HttpLocust, TaskSet, task

from helper import get_logger

logger = get_logger(__name__)

users = [{
    "username": "mazimia",
    "email": "mazimia@gmail.com",
    "first_name": "Mazimia",
    "password": "selfi12"
}, {
    "username": "mazimia1",
    "email": "mazimia1@gmail.com",
    "first_name": "Mazimia2",
    "password": "selfi12"
}, {
    "username": "mazimia2",
    "email": "mazimia2@gmail.com",
    "first_name": "Mazimia2",
    "password": "selfi12"
}, {
    "username": "mazimia3",
    "email": "mazimia3@gmail.com",
    "first_name": "Mazimia3",
    "password": "selfi12"
}]


class UserBehavior(TaskSet):

    token = None
    user_name = None
    flight_id = None

    @task
    class SubClass(TaskSet):
        @task(1)
        def book_flight(self):
            self.client.patch(
                f"v1/flights/{UserBehavior.flight_id}/book_flight/",
                data={"username": UserBehavior.user_name},
                headers={"Authorization": f"Bearer {UserBehavior.token}"})

    def on_start(self):
        """ on_start is called when a Locust starts."""
        response = self.login()
        self.admin_token = self.admin_login()
        UserBehavior.token = response.json()["access"]
        UserBehavior.user_name = response.json()["username"]

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        pass

    @task(5)
    def index(self):
        self.client.get("")

    def login(self):
        if len(users) > 0:
            user = users.pop(0)
            # Signup user
            self.client.post("account/users/", data=user)
            detail = {
                "username": user["username"],
                "password": user["password"]
            }
            # login user
            response = self.client.post("account/login/", data=detail)
            return response

    def admin_login(self):
        detail = {
            "username": "touchstone",
            "password": os.environ["ADMIN_PASS"]
        }
        response = self.client.post("account/login/", data=detail)
        return response.json()["access"]

    @task(5)
    def get_flights(self):
        """Load tests for getting flights."""
        self.client.get("v1/flights/")

    @task(5)
    def create_flights(self):
        """Load tests for creating flights."""
        response = self.client.post(
            "v1/flights/",
            data={
                "origin": "Lagos",
                "destination": "Chicago",
                "departure_date": timedelta(days=1) + datetime.utcnow().date(),
                "plane_type": "economic",
            },
            headers={"Authorization": f"Bearer {self.admin_token}"})
        UserBehavior.flight_id = response.json()["id"]


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000  # milliseconds
    max_wait = 9000  # milliseconds
