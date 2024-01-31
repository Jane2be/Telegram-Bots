import telebot
from currency_converter import CurrencyConverter
from telebot import types

amount = 0

bot = telebot.TeleBot("5890451657:AAGhICqq2wJCbg5oc3DL6CCte965_bO7MLc")
currency = CurrencyConverter()

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Hi! Type in the amount.")
    bot.register_next_step_handler(message,summa)

def summa(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, "Wrong format. Type in a number.")
        bot.register_next_step_handler(message, summa)
        return

    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton("USD/EUR", callback_data="usd/eur")
        btn2 = types.InlineKeyboardButton("EUR/USD", callback_data="eur/usd")
        btn3 = types.InlineKeyboardButton("USD/GBP", callback_data="usd/gbp")
        btn4 = types.InlineKeyboardButton("Other", callback_data="else")
        markup.add(btn1,btn2,btn3,btn4)
        bot.send_message(message.chat.id, "Select currencies.", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "The amount must be bigger than 0.")
        bot.register_next_step_handler(message, summa)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != "else":
        values = call.data.upper().split("/")
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f"It's {round(res, 2)}.\nType in new amount.")
        bot.register_next_step_handler(call.message, summa)
    else:
        bot.send_message(call.message.chat.id, "Type in two currencies in 'CUR1/CUR2' format")
        bot.register_next_step_handler(call.message, my_currency)

def my_currency(message):
        try:
            values = message.text.upper().split("/")
            res = currency.convert(amount, values[0], values[1])
            bot.send_message(message.chat.id, f"It's {round(res, 2)}.\nType in new amount.")
            bot.register_next_step_handler(message, summa)
        except Exception:
            bot.send_message(message.chat.id, "Wrong format. Try again.")
            bot.register_next_step_handler(message, my_currency)
    

bot.polling(non_stop=True)