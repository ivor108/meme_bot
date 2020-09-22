from apscheduler.schedulers.blocking import BlockingScheduler
from memes import get_memes
import config
import random

sched = BlockingScheduler()
c = 0
@sched.scheduled_job('interval', minutes=1)
def timed_job():
    global c
    c = c + 1
    print('MEMES update!')

def get_random_meme():
    return random.choice(c)

sched.start()