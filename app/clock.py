"""schedule jobs for heroku scheduler."""

from apscheduler.schedulers.blocking import BlockingScheduler

from api.mail import send_mail_notifications

sched = BlockingScheduler()


@sched.scheduled_job('interval', hour=24)
def run_daily():
    send_mail_notifications()


sched.start()
