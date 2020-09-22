from apscheduler.schedulers.blocking import BlockingScheduler
from memes import get_memes
import config
import random

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def timed_job():
    print('MEMES update!')

sched.start()