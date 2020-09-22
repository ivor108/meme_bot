from apscheduler.schedulers.blocking import BlockingScheduler
from main import bot

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def timed_job():
    print('This job is run every one minutes.')
    bot.send_message(414011250, 'я тут!')

sched.start()