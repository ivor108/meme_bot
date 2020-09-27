from apscheduler.schedulers.background import BackgroundScheduler
from memes import get_memes
import config
import random

sched = BackgroundScheduler()

@sched.scheduled_job('interval', minutes=1)
def timed_job():
    print('MEMES update!')

sched.start()