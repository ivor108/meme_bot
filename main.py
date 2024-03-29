import telebot
from rate import get_rate
from weather import get_weather
from memes import get_memes, get_random_meme
from apscheduler.schedulers.background import BackgroundScheduler
from dota import *
#from covid import *

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
dota_keyboard = telebot.types.ReplyKeyboardMarkup(True)
covid_keyboard = telebot.types.ReplyKeyboardMarkup(True)

main_keyboard.row('Развлечения', 'Что происходит?', 'Расскажи о себе')
city_keyboard.row('Дубна', 'Москва', 'Санкт-Петербург')
fun_keyboard.row('Мем', 'Дота')  # сюда нужно еще что-нибудь добавить
news_keyboard.row('Что с рублем?', 'Погода')
covid_keyboard.row('Сша', 'Россия', 'Италия', 'Япония')
create_dota_keybord(dota_keyboard)

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
        bot.send_message(message.chat.id, 'В данный момент я могу скидывать мемы и информацию о доте', reply_markup=fun_keyboard)
    elif message.text.lower() == 'мем':
        send_mem(message.chat.id, get_random_meme())
    elif message.text.lower() == 'что происходит?':
        bot.send_message(message.chat.id, 'Ты можешь узнать курсы валют, прогноз погоды и информацию о Covid-19', reply_markup=news_keyboard)
    elif message.text.lower() == 'что с рублем?':
        bot.send_message(message.chat.id, get_rate(), reply_markup=main_keyboard)
    elif message.text.lower() == 'погода':
        bot.send_message(message.chat.id, 'Напиши свой город', reply_markup=city_keyboard)
        bot.register_next_step_handler(message, choice_city)
    elif message.text.lower() == 'расскажи о себе':
        bot.send_message(message.chat.id, 'Привет, я могу скидывать мемы. Так же у меня можно узнать актуальные новости и посмотреть какого героя выбрать в доте!')
    elif message.text.lower() == 'дота':
        bot.send_message(message.chat.id, 'Напиши имя героя', reply_markup=dota_keyboard)
        bot.register_next_step_handler(message, choice_dota)
    else:
        bot.send_message(message.chat.id, 'Не понимаю!')


def choice_city(message):
    bot.send_message(message.chat.id, get_weather(message.text), reply_markup=main_keyboard)


def choice_dota(message):
    try:
        best, worst = get_best_wors_picks(message.text)
        str_best = ""
        str_worst = ""
        for i in range(len(best)):

            for j in range(len(best[0])):
                str_best += best[i][j] + " "
                str_worst += worst[i][j] + " "
            str_best += "\n"
            str_worst += "\n"
        str_all ="Лучший пик\n" + str_best + "\nХудший пик\n" + str_worst
        bot.send_message(message.chat.id, str_all,  reply_markup=main_keyboard)
    except:
        bot.send_message(message.chat.id, 'Неправильное имя героя',  reply_markup=main_keyboard)

def choice_country(message):
    try:
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAIgT1-A4QeHcYRTjLeh7Q35tkpYaU2IAAIZBgACu-LZS7x-ZyzJUUkPGwQ')
        #bot.send_message(message.chat.id, getcorona(message.text), reply_markup=main_keyboard)
    except:
        bot.send_message(message.chat.id, 'Ошибка библиотеки',  reply_markup=main_keyboard)

bot.polling()
