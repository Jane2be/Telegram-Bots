import telebot
from telebot import types
from random import randint

bot = telebot.TeleBot("OUR_BOT_TOKEN")

#проверка типа файла
@bot.message_handler(content_types=["photo", "video", "audio"])
def get_file(message):
    #кнопки
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Get help", callback_data="help")
    markup.row(button1)
    bot.reply_to(message, "Sorry I don't understand...", reply_markup=markup)

#действия кнопок
@bot.callback_query_handler(func= lambda callback: True)
def callback_message(callback):
    if callback.data == "help":
        bot.send_message(callback.message.chat.id, "Press /card to get your card of the day.")
    elif callback.data == "more":
        pass

#обработка комманд
@bot.message_handler(commands=["start", "card"])
def main(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("One more", callback_data="more"))
    card_num = randint(0,11)
    card = open(f"{card_num}.png", "rb")
    bot.send_message(message.chat.id, f"<b>Hello</b>, {message.from_user.first_name}! Here is your card of the day.", parse_mode="html")
    bot.send_photo(message.chat.id, card)
    if card_num == 0:
        bot.send_message(message.chat.id, "The Fool is a card of new beginnings, opportunity and potential. Just like the young man, you are at the outset of your journey, standing at the cliff‘s edge, and about to take your first step into the unknown.")
    if card_num == 1:
        bot.send_message(message.chat.id, "The Magician brings you the tools, resources and energy you need to make your dreams come true. Seriously, everything you need right now is at your fingertips.")
    if card_num == 2:
        bot.send_message(message.chat.id, "The High Priestess teaches you that the world is not always as it seems and more profound influences are often at play. She ushers you through the thin veil of awareness, offering you a deep, intuitive understanding of the Universe and a heightened awareness of secret or hidden information.")
    if card_num == 3:
        bot.send_message(message.chat.id, "The Empress signifies a strong connection with our femininity. She calls on you to connect with your feminine energy. Create beauty in your life. Connect with your senses through taste, touch, sound, smell and sight. ")
    if card_num == 4:
        bot.send_message(message.chat.id, "As the father figure of the Tarot deck, The Emperor suggests that you are adopting this fatherly role (regardless of whether you are male or female), providing for your family, and protecting and defending your loved ones.")
    if card_num == 5:
        bot.send_message(message.chat.id, "The Hierophant card represents an established set of spiritual values and beliefs and is often correlated with religion and other formal doctrines. Before you can discover your own belief systems and make your own choices, The Hierophant encourages you to learn the fundamental principles from a trusted source.")
    if card_num == 6:
        bot.send_message(message.chat.id, "The Lovers card represents conscious connections and meaningful relationships. It shows that you have a beautiful, soul-honoring connection with a loved one. It can also represent a close friendship or family relationship where love, respect and compassion flow.")
    if card_num == 7:
        bot.send_message(message.chat.id, "The Chariot is a card of willpower, determination, and strength. You have discovered how to make decisions in alignment with your values, and now you are taking action on those decisions. Take it as a sign of encouragement.")
    if card_num == 8:
        bot.send_message(message.chat.id, "The Strength card represents strength, determination, and power. It speaks to the inner strength and the human spirit's ability to overcome any obstacle. Strength is about knowing you can endure life’s obstacles. You have great stamina and persistence, balanced with underlying patience and inner calm.")
    if card_num == 9:
        bot.send_message(message.chat.id, "The Hermit shows that you are taking a break from everyday life to draw your energy and attention inward and find the answers you seek, deep within your soul. ")
    if card_num == 10:
        bot.send_message(message.chat.id, "The Wheel of Fortune reminds you that the wheel is always turning and life is in a state of constant change. If you're going through a difficult time rest assured that it will get better from here. Good luck and good fortune will make their return in time.")

#обработка комманд
@bot.message_handler(commands=["help"])
def main(message):
    bot.send_message(message.chat.id, "Press /card to get your card of the day.")

#обработка просто текста, после комманд
@bot.message_handler()
def info(message):
    if message.text.lower() in "hello, hi":
        bot.send_message(message.chat.id, f"<b>Hello</b>, {message.from_user.first_name}!", parse_mode="html")
    elif "id" in message.text.lower():
        #ответ на предыдущее сообщение
        bot.reply_to(message, f"ID: {message.from_user.id}")
    else:
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton("Get help", callback_data="help")
        markup.row(button1)
        bot.reply_to(message, "Sorry I don't understand...", reply_markup=markup)


bot.polling(non_stop=False)

