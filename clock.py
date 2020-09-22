from apscheduler.schedulers.blocking import BlockingScheduler
from main import bot
from config import MEMES
from memes import get_memes

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def timed_job():
    MEMES = get_memes()
    print('MEMES update!')

sched.start()