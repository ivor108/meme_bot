import requests
import json
from geopy.geocoders import Nominatim
import os

def get_weather(city):
	geolocator = Nominatim(user_agent="weather-bot")
	location = geolocator.geocode(city)

	lat = location.latitude
	long = location.longitude
	try:
		weather_req = requests.get('https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&appid={}'.format(lat, long, os.environ.get("WEATHER_KEY")))
		if weather_req.status_code == 200:
			current_weather = json.loads(weather_req.text)['current']
			temp = round(current_weather['temp'] - 273.15)
			feels_like = round(current_weather['feels_like'] - 273.15)
			clouds = current_weather['clouds']
			wind_speed = current_weather['wind_speed']
		else:
			print("[-] Can't get access to openweathermap")
	except Exception as e:
		print("[-] Can't get the weather: ", e)

	if temp && feels_like && clouds && wind_speed:
		return 'Сейчас температура воздуха - {} градусов, ощущается как {} градусов, облачность - {}%, скорость ветра - {}м/с'.format(str(temp), str(feels_like), str(clouds), str(wind_speed))
	else:
		print("[-] Something went wrong in weather class")