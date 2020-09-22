from apscheduler.schedulers.blocking import BlockingScheduler
from memes import get_memes

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def timed_job():
    #get_memes()
    print('MEMES update!')

sched.start()