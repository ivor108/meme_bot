import telebot
from rate import get_rate
from weather import get_weather
from memes import get_memes, get_random_meme
from apscheduler.schedulers.background import BackgroundScheduler
from dota import *

import psycopg2
import os
import requests

conn = psycopg2.connect(os.environ.get("DATABASE_URL"), sslmode='require')
cur = conn.cursor()

sched = BackgroundScheduler()

bot = telebot.TeleBot(os.environ.get("TOKEN"))

main_keyboard = telebot.types.ReplyKeyboardMarkup(True)
city_keyboard = telebot.types.ReplyKeyboardMarkup(True)
fun_keyboard = telebot.types.ReplyKeyboardMarkup(True)
news_keyboard = telebot.types.ReplyKeyboardMarkup(True)


main_keyboard.row('Развлечения','Что происходит?', 'Расскажи о себе')
city_keyboard.row('Дубна', 'Москва', 'Санкт-Петербург')
fun_keyboard.row('Мем') #сюда нужно еще что-нибудь добавить
news_keyboard.row('Что с рублем?', 'Погода')

def send_mem(chatid, mem):
    r = requests.get(mem[1])
    with open('img.jpg', 'wb') as fd:
        for chunk in r.iter_content(1):
            fd.write(chunk)
    photo = open('img.jpg', 'rb')
    bot.send_photo(chatid, photo, caption=mem[0], reply_markup=main_keyboard)
    os.remove('img.jpg')

@sched.scheduled_job('interval', minutes=30)
def hello():
    get_memes()
    print('Memes uploaded!')
sched.start()

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start', reply_markup=main_keyboard)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'развлечения':
        bot.send_message(message.chat.id, 'В данный момент я могу только скидывать мемы', reply_markup=fun_keyboard)
    elif message.text.lower() == 'мем':
        send_mem(message.chat.id, get_random_meme())
    elif message.text.lower() == 'что происходит?':
        bot.send_message(message.chat.id, 'Ты можешь узнать курсы валют или прогноз погоды', reply_markup=news_keyboard)
    elif message.text.lower() == 'что с рублем?':
        bot.send_message(message.chat.id, get_rate(), reply_markup=main_keyboard)
    elif message.text.lower() == 'погода':
        bot.send_message(message.chat.id, 'Напиши свой город', reply_markup=city_keyboard)
        bot.register_next_step_handler(message, choice_city)
    elif message.text.lower() == 'расскажи о себе':
        bot.send_message(message.chat.id, 'У меня новое обновление! Мемы загружаются быстрее. Теперь я могу скидывать топ мемов недели!')
    elif message.text.lower() == 'дота':
        best, worst = get_best_wors_picks('abaddon')
        bot.send_message(message.chat.id, best[0][0])
        bot.send_message(message.chat.id, best[0][1])
        bot.send_message(message.chat.id, best[0][2])
    else:
        bot.send_message(message.chat.id, 'Не понимаю!')


def choice_city(message):
    bot.send_message(message.chat.id, get_weather(message.text), reply_markup=main_keyboard)


bot.polling()
