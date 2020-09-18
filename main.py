import telebot
import random
import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
import os
import time
#from rate import rate

URL = 'https://www.reddit.com/r/memes/'
HEADERS = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'}

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
driver.get(URL)

bot = telebot.TeleBot('1345384313:AAFfCxtgq-iici7UBN0C1A4YZ-ylxs1Z_cY')
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
        bot.send_message(message.chat.id, get_memes())
    elif message.text.lower() == 'rate':
        bot.send_message(message.chat.id, rate())
    elif message.text.lower() == 'расскажи о себе':
        bot.send_message(message.chat.id, 'Теперь можно смотреть курсы валют!')
    else:
        bot.send_message(message.chat.id, 'Не понимаю!')
   
'''
#Старые методы для парсинга
def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS)
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
'''

def get_memes():
    memes = []
    SCROLL_PAUSE_TIME = 0.5
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    elements = driver.find_elements_by_class_name('_2_tDEnGMLxpM6uOa2kaDB3._1XWObl-3b9tPy64oaG6fax')

    for element in elements:
        mem = element.get_attribute('src')
        if str(mem).count('external') == 0:
            memes.append(str(mem))
            print(mem)

    return (memes.pop())


def rate(): # Понятия не имею зачем это нужно
    USD_URL = 'https://finance.rambler.ru/currencies/USD/'
    EUR_URL = 'https://finance.rambler.ru/currencies/EUR/'
    BTC_URL = 'https://ru.investing.com/crypto/bitcoin/btc-usd'
    req_USD = requests.get(USD_URL)
    req_EUR = requests.get(EUR_URL)
    req_BTC = requests.get(BTC_URL,  headers=HEADERS)
    USD = re.search('<div class="finance-currency-plate__currency">([\w\W]*?)<\/div>', req_USD.text).group(1)
    EUR = re.search('<div class="finance-currency-plate__currency">([\w\W]*?)<\/div>', req_EUR.text).group(1)
    BTC = re.search('id="last_last" dir="ltr">([\w\W]*?)<', req_BTC.text).group(1)
    USD = re.sub("^\s+|\n|\r|\s+$", '', USD)
    EUR = re.sub("^\s+|\n|\r|\s+$", '', EUR)
    return str('$ {}\n'.format(USD))+str('€ {}\n'.format(EUR))+str('BTC {}'.format(BTC))




bot.polling()