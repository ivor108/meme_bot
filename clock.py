from apscheduler.schedulers.blocking import BlockingScheduler
from memes import get_memes
import config
import random

sched = BlockingScheduler()
MEMES = []
@sched.scheduled_job('interval', minutes=2)
def timed_job():
    global MEMES
    MEMES = get_memes()
    print('MEMES update!')
    print(MEMES)

def get_random_meme():
    return random.choice(MEMES)

sched.start()