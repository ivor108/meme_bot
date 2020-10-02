import requests
from bs4 import BeautifulSoup

URL = 'https://volga-volga.dubna.ru/'
req = requests.get(URL)

soup = BeautifulSoup(req.text, 'lxml')

movie = soup.find_all('h2', {'class':'sc-1h5tg87-0 jgRCED title'})
age = soup.find_all('div', class_='sc-AxjAm sc-AxirZ ezTcmd sc-9rykaf-0 jPAGcr tags')

for i in movie:
	for j in age:
		print i.text + ' ' + j.text





