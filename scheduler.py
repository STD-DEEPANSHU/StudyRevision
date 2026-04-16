from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from config import START_HOUR, END_HOUR, SEND_INTERVAL_MINUTES

scheduler = BackgroundScheduler()

def can_send():
    now = datetime.now().hour
    return START_HOUR <= now <= END_HOUR

def start_scheduler(send_function):
    scheduler.add_job(
        send_function,
        'interval',
        minutes=SEND_INTERVAL_MINUTES,
        max_instances=1,
        coalesce=True
    )
    scheduler.start()
