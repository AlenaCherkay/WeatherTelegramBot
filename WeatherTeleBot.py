import json
import random

import telebot
import requests

from telebot import types

token = '...'
bot = telebot.TeleBot(token)
API = '...'

# @bot.message_handler(commands=['start'])
# def main(message):
#   bot.send_message(message.chat.id, 'Привет, напиши название города')

WEATHER_DICT = {
  'clear sky':'Ясно',
  'few clouds':'Местами облачно',
  'scattered clouds':'Облачно',
  'broken clouds':'Пасмурно',
  'shower rain':'Пасмурно с осадками',
  'rain':'Дождь',
  'thunderstorm':'Гроза',
  'snow':'Снег',
  'mist':'Туман',
}
PICTURE_DICT = {
  '01d' : 'pict/01d.png',
  '01n' : 'pict/01n.png',
  '02d' : 'pict/02d.png',
  '02n' : 'pict/02n.png',
  '03d' : 'pict/03nd.png',
  '03n' : 'pict/03nd.png',
  '04d' : 'pict/04nd.png',
  '04n' : 'pict/04nd.png',
  '09d' : 'pict/09nd.png',
  '09n' : 'pict/09nd.png',
  '10d' : 'pict/10d.png',
  '10n' : 'pict/10n.png',
  '11d' : 'pict/11d.png',
  '11n' : 'pict/11n.png',
  '13d' : 'pict/13d.png',
  '13n' : 'pict/13n.png',
  '50d' : 'pict/50nd.png',
  '50n' : 'pict/50nd.png',
}

STICKER_PACK = [
  'CAACAgIAAxkBAAIDcGYmojRJStue45OQ8Vx5zwNWq3-hAAJxGAACYCzASEMSepqSzWQgNAQ',
  'CAACAgIAAxkBAAIDcWYmoj1bnsA9TIl91ZoJ44Ly0YBiAAIZAAPp2BMoV2ES2mxgqss0BA',
  'CAACAgIAAxkBAAIDcmYmokHp9gngkgywhWtH8zr8DjtOAAI2PgACl_aZSy-bOrbhl7S6NAQ',
  'CAACAgIAAxkBAAIDc2YmokRF6rT5vvc1oDATl4wuH6cZAALRPAACtt9oSL0fERcJysxxNAQ',
  'CAACAgIAAxkBAAIDdGYmory7XYoHO5NVjkSwgi5qxth0AAK1QwAC5YFhSM_nctl8F-vZNAQ',
  'CAACAgIAAxkBAAIDdWYmos_sA-_oneb2M85M_-rWfiZrAAIqRwACYdpoSKsAAQ2QWBSuaDQE'
]


@bot.message_handler(commands=['start'])
def main(message):
  """
    Функция отвечает на комаду /start. Выводит сообщение, отправляет стикер и добавляет три кнопки
  """
  markup = types.InlineKeyboardMarkup()
  btn1 = types.InlineKeyboardButton("Погода от яндекса", url='https://yandex.ru/pogoda')
  btn2 = types.InlineKeyboardButton("Узнать погоду в любом городе", callback_data='weather')
  btn3 = types.InlineKeyboardButton("Посмотреть локацию", url='https://2gis.ru')
  markup.row(btn2)
  markup.row(btn1,btn3)

  bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}\n"
                                    f"Можешь посмотреть погоду в своем городе,"
                                    f"открыть карты если тебе нужен навигатор,"
                                    f"или же посмотреть погоду в любой точке мира."
                                    f"Дерзай", reply_markup = markup)

  rand_sticker = random.choice(STICKER_PACK)
  bot.send_sticker(message.chat.id, rand_sticker)

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
  """
    Функция callback. Срабатывает при выборе кнопки со значением 'weather'
    Запрашивает город, подключается к API и выводит информацию
  """

  if callback.data == 'weather':
    bot.send_message(callback.message.chat.id,'Введите город')
    @bot.message_handler(content_types=['text'])
    def get_weather(message):
      city = message.text.strip().lower()
      res = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric")
      if res.status_code == 200:
        data = json.loads(res.text)
        weather_data = data['weather'][0]
        weather_disc = weather_data['description']
        pic = weather_data['icon']
        wind = data['wind']['speed']
        file = open(PICTURE_DICT.get(pic, 'pict/1.png'), 'rb')

        bot.reply_to(message, f'Погода - <b>{city.capitalize()}</b> :\n\n'
                              f'{WEATHER_DICT.get(weather_disc, "Температура:")} {round(data["main"]["temp"])} °C\n'
                              f'Ощущается как {round(data["main"]["feels_like"])} °C\n\n'
                              f'Ветер: {wind} м\с \n', parse_mode="html")

        bot.send_photo(message.chat.id, file)
      else:
        bot.reply_to(message, 'Город указан неверно')

  elif callback.data == 'edit':
    bot.edit_message_text('Edit text', callback.message.chat.id, callback.message.message_id)

bot.infinity_polling()