import requests
from bs4 import BeautifulSoup
from config import *

def get_rate():
	try:
		req_USD = requests.get(USD_URL, headers=HEADERS)
		if req_USD.status_code == 200:
			soup = BeautifulSoup(req_USD.text, 'lxml')
			USD = soup.find('span', class_='DFlfde SwHCTb')
		else:
			print("[-] Can't get access to website to get the USD rate")
	except Exception as e:
		print("[-] Can't get the USD rate: ", e)

	try:
		req_EUR = requests.get(EUR_URL, headers=HEADERS)
		if req_EUR.status_code == 200:
			soup = BeautifulSoup(req_EUR.text, 'lxml')
			EUR = soup.find('span', class_='DFlfde SwHCTb')
		else:
			print ("[-] Can't get access to website to get the EUR rate")
	except Exception as e:
		print("[-] Can't get the EUR rate: ", e)

	try:
		req_BTC = requests.get(BTC_URL, headers=HEADERS)
		if req_EUR.status_code == 200:
			soup = BeautifulSoup(req_BTC.text, 'lxml')
			BTC = soup.find('span', class_='DFlfde SwHCTb')
		else:
			print("[-] Can't get access to website to get the BTC rate")
	except Exception as e:
		print("[-] Can't get the BTC rate: ", e)

	if USD and EUR and BTC:
		return '$ {}₽\n'.format(USD.text) + '€ {}₽\n'.format(EUR.text) + '₿ {}₽'.format(BTC.text)
	else:
		print("[-] Something went wrong in rate class")