from apscheduler.schedulers.blocking import BlockingScheduler
from memes import get_memes
import config

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def timed_job():
    config.MEMES = get_memes()
    print('MEMES update!')
    print(config.MEMES)

sched.start()