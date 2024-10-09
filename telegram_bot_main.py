import requests
import telebot
from local_settings import API_TOKEN, APPID

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Напиши название город и я скажу какая там погода\
""")


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def city_weather_today_message(message):
    city = str(message.text)
    print(city)
    try:
        response = requests.get(
            f'https://api.openweathermap.org/data/2.5/find?q={city}&type=like&APPID={APPID}&units=metric'
        )
        weather_data = response.json()['list']
        print(weather_data)
        for city_data in weather_data:
            bot.send_message(message.chat.id, f"""Today weather in {city}\
                            {city_data['main']['temp']}\
                            {city_data['main']['temp_min']}\
                            {city_data['main']['temp_max']}""")
            break
    except Exception as exception:
        print("Exception (find):", exception)
        bot.send_message(message.chat.id, 'Такого города не существует')


bot.infinity_polling()
