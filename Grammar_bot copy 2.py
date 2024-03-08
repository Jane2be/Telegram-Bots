import telebot
from telebot import types
from random import choice

bot = telebot.TeleBot("OUR_BOT_TOKEN")

#проверка типа файла
@bot.message_handler(content_types=["photo", "video", "audio"])
def get_file(message):
    #кнопки
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Get help", callback_data="help")
    button2 = types.InlineKeyboardButton("Delete", callback_data="delete")
    markup.row(button1, button2)
    bot.reply_to(message, "Sorry I don't understand...", reply_markup=markup)

#действия кнопок
@bot.callback_query_handler(func= lambda callback: True)
def callback_message(callback):
    are_list = ["You", "We", "They", "My friends and I", "Sarah and John"]
    is_list = ["He", "She", "It", "Lucy", "My dog", "Michael"]
    wrong = " - wrong. Try again"
    correct = "Correct!⭐ The answer: "
    if callback.data == "delete":
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    elif callback.data == "help":
        bot.send_message(callback.message.chat.id, "Press /start to get a sentence.")
    elif callback.data == "more":
        pass
    elif callback.data == "am":
        if callback.message.text.split(" __ ")[0] in are_list:
            bot.reply_to(callback.message, f"❌ {callback.data}{wrong}")
        elif callback.message.text.split(" __ ")[0] in is_list:
            bot.reply_to(callback.message, f"❌ {callback.data}{wrong}")
        elif "I" == callback.message.text.split(" __ ")[0]:
            bot.reply_to(callback.message, f"{correct}{callback.data}")
    elif callback.data == "are":
        if callback.message.text.split(" __ ")[0] in are_list:
            bot.reply_to(callback.message, f"{correct}{callback.data}.")
        elif callback.message.text.split(" __ ")[0] in is_list:
            bot.reply_to(callback.message, f"❌ {callback.data}{wrong}")
        elif "I" == callback.message.text.split(" __ ")[0]:
            bot.reply_to(callback.message, f"❌ {callback.data}{wrong}")
    elif callback.data == "is":
        if callback.message.text.split(" __ ")[0] in is_list:
            bot.reply_to(callback.message, f"{correct}{callback.data}.")
        elif callback.message.text.split(" __ ")[0] in are_list:
            bot.reply_to(callback.message, f"❌ {callback.data}{wrong}")
        elif "I" == callback.message.text.split(" __ ")[0]:
            bot.reply_to(callback.message, f"❌ {callback.data}{wrong}")
    elif callback.data == "a":
        if callback.message.text.split(" __ ")[1][0] in "auoei":
            bot.reply_to(callback.message, f"❌ {callback.data}{wrong}")
        else:
            bot.reply_to(callback.message, f"{correct}{callback.data}.")
    elif callback.data == "an":
        if callback.message.text.split(" __ ")[1][0] not in "auoei":
            bot.reply_to(callback.message, f"❌ {callback.data}{wrong}")
        else:
            bot.reply_to(callback.message, f"{correct}{callback.data}.")


#кнопки вместо клавиатуры
@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("to be in Present Simple")
    button2 = types.KeyboardButton("a / an")
    #button3 = types.KeyboardButton("Present Simple")
    #button4 = types.KeyboardButton("Present Simple")
    #button5 = types.KeyboardButton("Present Simple")
    #button6 = types.KeyboardButton("More")
    markup.row(button1, button2)
    #markup.row(button4, button5, button6)
    bot.send_message(message.chat.id, "Choose a topic:", reply_markup=markup)
    bot.register_next_step_handler(message, on_click)

def on_click(message):
    if message.text == "to be in Present Simple":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Back")
        button2 = types.KeyboardButton("One more")
        markup.row(button2, button1)
        bot.send_message(message.chat.id, "Press One more to get a sentence.")
        bot.send_message(message.chat.id, "If you want to choose another topic, press Back button below.", reply_markup=markup)
        bot.register_next_step_handler(message, on_click)
    if message.text == "Back":
        start(message)
    if message.text == "One more":
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton("am", callback_data="am")
        button2 = types.InlineKeyboardButton("are", callback_data="are")
        button3 = types.InlineKeyboardButton("is", callback_data="is")
        markup.row(button1, button2, button3)
        subjects = ["I", "You", "He", "She", "It", "We", "They", "Lucy", "My friends and I", "My dog", "Sarah and John", "Michael"]
        objects = ["cute.", "happy.", "in a hotel.", "late.", "at work.", "Japanese.", "not in London.", "29.", "on time.", "old.", "from Spain.", "not from Italy.", "not at home.", "in the UK."]
        bot.send_message(message.chat.id, choice(subjects) + " __ " + choice(objects), reply_markup=markup)
        bot.register_next_step_handler(message, on_click)
    if message.text == "a / an":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Back")
        button2 = types.KeyboardButton("Next")
        markup.row(button2, button1)
        bot.send_message(message.chat.id, "Press Next to get a sentence.")
        bot.send_message(message.chat.id, "If you want to choose another topic, press Back button below.", reply_markup=markup)
        bot.register_next_step_handler(message, on_click)
    if message.text == "Next":
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton("a", callback_data="a")
        button2 = types.InlineKeyboardButton("an", callback_data="an")
        markup.row(button1, button2)
        subjects = ["It's", "It's", "I'm", "He's", "She's", "Lucy's",  "My mother is", "Her brother is", "His neighbour is"]
        jobs = ["football player.", "doctor.", "school teacher.", "pilot.", "farmer.", "nurse.", "taxi driver.", "office worker.", "artist.", "architect.", "dentist.", "receptionist.", "astronaut.", "accountant.", "programmer."]
        objects = ["ball.", "computer.", "backpack.", "credit card.", "handbag.", "keyboard.", "laptop.", "newspaper.", "passport.", "screen.", "umbrella.", "wallet."]
        subject = choice(subjects)
        if subject == "It's":
            bot.send_message(message.chat.id, subject + " __ " + choice(objects), reply_markup=markup)

        else:
            bot.send_message(message.chat.id, subject + " __ " + choice(jobs), reply_markup=markup)
        bot.register_next_step_handler(message, on_click)







#обработка комманд
@bot.message_handler(commands=["help"])
def main(message):
    bot.send_message(message.chat.id, "Press /start to open the main menu.")

#обработка просто текста, после комманд
@bot.message_handler()
def info(message):
    if message.text.lower() in "hello, hi":
        bot.send_message(message.chat.id, f"<b>Hello</b>, {message.from_user.first_name}!", parse_mode="html")
    else:
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton("Get help", callback_data="help")
        markup.row(button1)
        bot.reply_to(message, "Sorry I don't understand...", reply_markup=markup)


bot.polling(non_stop=True)
