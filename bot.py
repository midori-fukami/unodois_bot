# import telebot
# import os
# from dotenv import load_dotenv

# load_dotenv()

# BOT_TOKEN = os.environ["BOT_TOKEN"]

# bot = telebot.TeleBot(BOT_TOKEN)

# @bot.message_handler(commands=['start', 'hello'])
# def send_welcome(message):
#     bot.reply_to(message, "Howdy, how are you doing?")

# @bot.message_handler(func=lambda msg: True)
# def echo_all(message):
#     bot.reply_to(message, message.text)

# bot.infinity_polling()