from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from config import START_HOUR, END_HOUR, SEND_INTERVAL_HOURS

def can_send():
    now = datetime.now().hour
    return START_HOUR <= now <= END_HOUR

def start_scheduler(send_function):
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_function, 'interval', hours=SEND_INTERVAL_HOURS)
    scheduler.start()
