from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from config import START_HOUR, END_HOUR, INTERVAL_MIN
from database import users
from bot import send_revision_to_user

scheduler = BackgroundScheduler()

def can_send():
    h = datetime.now().hour
    return START_HOUR <= h <= END_HOUR

def job():
    if not can_send():
        return

    for u in users.find():
        send_revision_to_user(u["user_id"])

def start():
    scheduler.add_job(
        job,
        'interval',
        minutes=INTERVAL_MIN,
        max_instances=1,
        coalesce=True
    )
    scheduler.start()
