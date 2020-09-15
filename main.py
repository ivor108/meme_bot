import telebot
import random
import requests
from bs4 import BeautifulSoup

URL = 'https://www.reddit.com/r/memes/'
HEADERS = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'}

bot = telebot.TeleBot('1345384313:AAFfCxtgq-iici7UBN0C1A4YZ-ylxs1Z_cY')
keyboard1 = telebot.types.ReplyKeyboardMarkup(True)
keyboard1.row('Привет', 'мем', 'расскажи о себе')

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start', reply_markup=keyboard1)

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Привет, я бот Максим, ты все понял')
    elif message.text.lower() == 'мем':
        bot.send_message(message.chat.id, get_memes())
    elif message.text.lower() == 'расскажи о себе':
        bot.send_message(message.chat.id, 'Я новый бот! Я буду скидывать мемы, если ты попросишь. Пока я могу скидвать только 4-5 мема, но каждые 2-3 часа этот список обновляется!')
    else:
        bot.send_message(message.chat.id, 'Не понимаю!')


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_memes():

    html = get_html(URL)
    if html.status_code == 200:
        return (random.choice(get_content(html.text)))
    else:
        print('Ошибка!')
        return (-1)

def get_content (html):
    soup = BeautifulSoup(html, 'html.parser')
    memes = []
    for items in soup.find_all(class_='_2_tDEnGMLxpM6uOa2kaDB3 ImageBox-image media-element _1XWObl-3b9tPy64oaG6fax'):
        if str(items.get('src')).count('external') == 0:
            memes.append(str(items.get('src')))
    print(memes)
    return (memes)

print('you lox')

bot.polling()