import requests
import re
from config import *

def get_rate(): # Понятия не имею зачем это нужно
    req_USD = requests.get(USD_URL)
    req_EUR = requests.get(EUR_URL)
    req_BTC = requests.get(BTC_URL,  headers=HEADERS)
    USD = re.search('<div class="finance-currency-plate__currency">([\w\W]*?)<\/div>', req_USD.text).group(1)
    EUR = re.search('<div class="finance-currency-plate__currency">([\w\W]*?)<\/div>', req_EUR.text).group(1)
    BTC = re.search('id="last_last" dir="ltr">([\w\W]*?)<', req_BTC.text).group(1)
    USD = re.sub("^\s+|\n|\r|\s+$", '', USD)
    EUR = re.sub("^\s+|\n|\r|\s+$", '', EUR)
    return str('$ {}\n'.format(USD))+str('€ {}\n'.format(EUR))+str('BTC {}'.format(BTC))