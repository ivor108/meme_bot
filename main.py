import telebot
import random
from rate import get_rate
from memes import get_memes, get_random_meme
from config import *
from apscheduler.schedulers.background import BackgroundScheduler

import psycopg2
import os
import requests

conn = psycopg2.connect(os.environ.get("DATABASE_URL"), sslmode='require')
cur = conn.cursor()

sched = BackgroundScheduler()

bot = telebot.TeleBot(TOKEN)
keyboard1 = telebot.types.ReplyKeyboardMarkup(True)
keyboard1.row('Привет', 'мем', 'расскажи о себе', 'rate')

def send_mem(chatid, mem):
    r = requests.get(mem[1])
    with open('img.jpg', 'wb') as fd:
        for chunk in r.iter_content(1):
            fd.write(chunk)
    photo = open('img.jpg', 'rb')
    bot.send_photo(chatid, photo, caption=mem[0])
    os.remove('img.jpg')

@sched.scheduled_job('interval', minutes=30)
def hello():
    get_memes()
    print('Memes uploaded!')
sched.start()

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start', reply_markup=keyboard1)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Привет, я бот Максим, ты все понял!')
    elif message.text.lower() == 'мем':
        send_mem(message.chat.id, get_random_meme())
    elif message.text.lower() == 'rate':
        bot.send_message(message.chat.id, get_rate())
    elif message.text.lower() == 'расскажи о себе':
        bot.send_message(message.chat.id, 'Теперь можно смотреть курсы валют!')
    elif message.text.lower() == 'id':
        bot.send_message(message.chat.id, message.chat.id)
    elif message.text.lower() == 'test':
        send_mem(message.chat.id, ('Raccoon vs. possum', 'https://preview.redd.it/ubxbvsy6a6p51.jpg?width=640&crop=smart&auto=webp&s=cc979c67732899b2ef2845025a02e866a0a2e17c'))
    else:
        bot.send_message(message.chat.id, 'Не понимаю!')



bot.polling()
