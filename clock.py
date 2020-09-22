from apscheduler.schedulers.blocking import BlockingScheduler
from memes import get_memes

MEMES = []
MEMES = get_memes()
sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def timed_job():
    global MEMES
    MEMES = get_memes()
    print('MEMES update!')

sched.start()