"""Define load testing for application."""

from locust import HttpLocust, TaskSet, task
from datetime import datetime, timedelta
from random import randint
from factory.faker import Faker


class UserBehavior(TaskSet):
    username = "allen"
    password = "allen1"

    def on_start(self):
        """ on_start is called when a Locust starts."""
        pass

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        pass

    @task
    def index(self):
        self.client.get("")

    @task
    def signup(self):
        """Signup a user."""
        self.client.post("account/users/",
                         data={
                             "username": Faker("last_name").generate(),
                             "email": Faker("email").generate(),
                             "first_name": Faker("first_name").generate(),
                             "password": f"user{randint(1, 1000)}"
                         })

    @task
    def login(self):
        self.client.post("account/login/",
                         data={
                             "username": self.username,
                             "password": self.password
                         })

    @task
    def get_flights(self):
        """Load tests for getting flights."""
        self.client.get("v1/flights/")

    @task
    def create_flights(self):
        """Load tests for creating flights."""
        self.client.post(
            "v1/flights/", {
                "origin": "Lagos",
                "destination": "Chicago",
                "departure_date": timedelta(days=1) + datetime.utcnow().date(),
                "plane_type": "economic"
            })


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 10000
