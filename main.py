import telebot
import random
from rate import get_rate
from memes import get_memes
from config import *
from clock import MEMES

bot = telebot.TeleBot(TOKEN)
keyboard1 = telebot.types.ReplyKeyboardMarkup(True)
keyboard1.row('Привет', 'мем', 'расскажи о себе', 'rate')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start', reply_markup=keyboard1)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Привет, я бот Максим, ты все понял!')
    elif message.text.lower() == 'мем':
        bot.send_message(message.chat.id, random.choice(MEMES))
    elif message.text.lower() == 'rate':
        bot.send_message(message.chat.id, get_rate())
    elif message.text.lower() == 'расскажи о себе':
        bot.send_message(message.chat.id, 'Теперь можно смотреть курсы валют!')
    elif message.text.lower() == 'id':
        bot.send_message(message.chat.id, message.chat.id)
    else:
        bot.send_message(message.chat.id, 'Не понимаю!')

bot.polling()
