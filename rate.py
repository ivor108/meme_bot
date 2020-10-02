import requests
from bs4 import BeautifulSoup
from config import *

def get_rate():
    req_USD = requests.get(USD_URL, headers=HEADERS)
    soup = BeautifulSoup(req_USD.text, 'lxml')
    USD = soup.find('span', class_='DFlfde SwHCTb')

    req_EUR = requests.get(EUR_URL, headers=HEADERS)
    soup = BeautifulSoup(req_EUR.text, 'lxml')
    EUR = soup.find('span', class_='DFlfde SwHCTb')

    req_BTC = requests.get(BTC_URL, headers=HEADERS)
    soup = BeautifulSoup(req_BTC.text, 'lxml')
    BTC = soup.find('span', class_='DFlfde SwHCTb')
    return '$ {}₽\n'.format(USD.text) + '€ {}₽\n'.format(EUR.text) + '₿ {}₽'.format(BTC.text)