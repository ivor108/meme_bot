import telebot
from rate import get_rate
from weather import get_weather
from memes import get_memes, get_random_meme, get_top_meme
from apscheduler.schedulers.background import BackgroundScheduler

import psycopg2
import os
import requests

conn = psycopg2.connect(os.environ.get("DATABASE_URL"), sslmode='require')
cur = conn.cursor()

sched = BackgroundScheduler()

bot = telebot.TeleBot(os.environ.get("TOKEN"))
keyboard1 = telebot.types.ReplyKeyboardMarkup(True)
keyboard2 = telebot.types.ReplyKeyboardMarkup(True)
keyboard3 = telebot.types.ReplyKeyboardMarkup(True)
keyboard1.row('Привет', 'мем','погода' 'расскажи о себе', 'Что с рублём?')
keyboard2.row('1', '2', '3')
keyboard3.row('Дубна', 'Москва', 'Санкт-Петербург')

def send_mem(chatid, mem):
    r = requests.get(mem[1])
    with open('img.jpg', 'wb') as fd:
        for chunk in r.iter_content(1):
            fd.write(chunk)
    photo = open('img.jpg', 'rb')
    bot.send_photo(chatid, photo, caption=mem[0], reply_markup=keyboard1)
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
    elif message.text.lower() == 'погода':
        bot.send_message(message.chat.id, 'Напиши свой город', reply_markup=keyboard3)
        bot.register_next_step_handler(message, choice_city)
    elif message.text.lower() == 'мем':
        send_mem(message.chat.id, get_random_meme())
    elif message.text.lower() == 'что с рублём?':
        bot.send_message(message.chat.id, get_rate())
    elif message.text.lower() == 'расскажи о себе':
        bot.send_message(message.chat.id, 'У меня новое обновление! Мемы загружаются быстрее. Теперь я могу скидывать топ мемов недели!')
    else:
        bot.send_message(message.chat.id, 'Не понимаю!')


def choice_city(message):
    bot.send_message(message.chat.id, get_weather(message.text), reply_markup=keyboard1)


bot.polling()
