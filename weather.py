import requests
import json
from geopy.geocoders import Nominatim
import os

def get_weather(city):
	geolocator = Nominatim(user_agent="weather-bot")
	location = geolocator.geocode(city)

	lat = location.latitude
	long = location.longitude

	weather_req = requests.get('https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&appid={}'.format(lat, long, environ.get("WEATHER_KEY")))

	current_weather = json.loads(weather_req.text)['current']
	temp = round(current_weather['temp'] - 273.15)
	feels_like = round(current_weather['feels_like'] - 273.15)
	clouds = current_weather['clouds']
	wind_speed = current_weather['wind_speed']

	return 'Сейчас температура воздуха - {} градусов, ощущается как {} градусов, облачность - {}%, скорость ветра - {}м/с'.format(str(temp), str(feels_like), str(clouds), str(wind_speed))
