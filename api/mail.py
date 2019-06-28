"""Define functionality that sends out mail notifications."""

from datetime import datetime, timedelta

from django.core import mail

from .models import Flight


def get_mail_notifications():
    """Generate list of emailmessage objects to send custom mails."""
    # Get all flights scheduled for at most one day to happen
    tomorrow = datetime.utcnow().date() + timedelta(days=1)
    scheduled_flights = Flight.records.filter(departure_date=tomorrow).all()
    subject = "Flight notification scheduled for {date}"
    body = """Hello {username}, your flight to {destination} from {origin}
        is scheduled for takeoff tomorrow, {departure_date}. Please don't miss
        it. Please log in to your account to confirm your take off time."""
    admin_mail = "flightbookie@gmail.com"
    # Create email_message for each flight passengers
    mail_messages = [
        mail.EmailMessage(subject=subject.format(date=flight.departure_date),
                          body=body.format(
                              username=passenger.username,
                              destination=flight.destination,
                              origin=flight.origin,
                              departure_date=flight.departure_date),
                          from_email=admin_mail,
                          to=["touchstone@gmail.com"],
                          bcc=[]) for flight in scheduled_flights
        for passenger in flight.passengers.all()
    ]
    return mail_messages


def send_mail_notifications():
    """Send emails notifying passengers of their flights."""
    connection = mail.get_connection()
    messages = get_mail_notifications()
    connection.send_messages(messages)
