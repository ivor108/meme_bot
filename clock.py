from apscheduler.schedulers.blocking import BlockingScheduler
from memes import get_memes
import config
import random

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def timed_job():
    memes = get_memes()
    MyFile = open('memes.txt', 'w')
    for mem in memes:
        print >>MyFile, mem
    MyFile.close()
    print('MEMES update!')

sched.start()