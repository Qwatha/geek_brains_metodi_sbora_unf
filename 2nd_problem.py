import requests
import json

s_city = input('Введите название города на английском: ')
appid = open("appid.env").read()


def get_сoordinates():
    req = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={s_city}&appid={appid}").json()
    lat = req[0]['lat']
    lon = req[0]['lon']
    return [lat, lon]


def get_weather(coor_list):
    lat, lon = coor_list
    req = requests.get(f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={appid}").json()
    return req['weather'][0]['main'], req['weather'][0]['description'], req['main']['temp']
