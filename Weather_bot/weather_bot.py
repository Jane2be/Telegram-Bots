import telebot
import urllib.request
import json
import urllib.parse

bot = telebot.TeleBot("5890451657:AAGhICqq2wJCbg5oc3DL6CCte965_bO7MLc")
API = 'ff6275d9ae24d29cfd3404474a66346e'

def get_weather(city):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric"
        res = urllib.request.urlopen(url)
        data = json.loads(res.read().decode('utf-8'))
        return data
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {"cod": "404"}
        else:
            raise

def send_weather_photo(chat_id, description):
    photo_dict = {
        "light rain": "rainy.png",
        "light intensity drizzle": "rainy.png",
        "light intensity shower": "rainy.png",
        "shower rain": "rainy.png",
        "rain": "rainy.png",
        "overcast clouds": "cloudy.png",
        "scattered clouds": "cloudy.png",
        "broken clouds": "cloudy.png",
        "few clouds": "cloudy.png",
        "clear sky": "sunny.png",
        "fog": "foggy.png",
        "mist": "foggy.png"
    }

    if description in photo_dict:
        file = open(photo_dict[description], "rb")
        bot.send_photo(chat_id, file)

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, f"Hello, {message.from_user.first_name}! Type in a city name.")

@bot.message_handler(content_types=["text"])
def handle_text(message):
    city = urllib.parse.quote(message.text.strip().lower())
    weather_data = get_weather(city)

    if weather_data["cod"] == "404":
        bot.reply_to(message, f"The city is not found. Try again.")
    else:
        temperature = round(weather_data['main']['temp'])
        weather_description = weather_data['weather'][0]['description']
        bot.reply_to(message, f"Now it's: {temperature} °С, {weather_description}.")
        send_weather_photo(message.chat.id, weather_description)

bot.polling(non_stop=False)

