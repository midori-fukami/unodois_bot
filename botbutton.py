from contextlib import nullcontext
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup

from aiogram.utils.markdown import hbold

from card import Card

from card import allCards
from player import Player

load_dotenv()

BOT_TOKEN = os.environ["BOT_TOKEN"]

bot = Bot(token=BOT_TOKEN)

dp = Dispatcher(bot)

lastCard = Card("1", "green")

allPlayers = []

# button1 = InlineKeyboardButton(text="button1", callback_data="In_First_button")
# button2 = InlineKeyboardButton(text="button2", callback_data="In_Second_button")
# keyboard_inline = InlineKeyboardMarkup().add(button1, button2)

@dp.callback_query_handler(text=["In_First_button", "In_Second_button"])
async def check_button(call: types.CallbackQuery):
    if call.data == "In_First_button":
        await call.message.answer("Hi! This is the first inline keyboard button.")
    if call.data == "In_Second_button":
        await call.message.answer("Hi! This is the second inline keyboard button.")
    await call.answer()

keyboard_reply = ReplyKeyboardMarkup(
	resize_keyboard=True, one_time_keyboard=True).add("players", "_button2")

@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    await message.reply("Hello! how are you?", reply_markup=keyboard_reply)

@dp.message_handler(commands=['new'])
async def new(message: types.Message):
    await message.reply("Created a new game! Join with /join and start with /start", reply_markup=keyboard_reply)

@dp.message_handler(commands=['join'])
async def join(message: types.Message):
    aux = []
    for x in allPlayers:
        aux.append(x.username)

    if message.from_user.username in aux:
        await message.reply(f"{message.from_user.username} already joined the game", reply_markup=keyboard_reply)
    else:
        addPlayer(message.from_user.first_name, message.from_user.username)
        await message.reply(f"{message.from_user.username} joined the game", reply_markup=keyboard_reply)
    # print(f"numero {allCards[4].number} e cor {allCards[4].color}")
    # print(f"total de cartas {len(allCards)}") #76?

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("First player", reply_markup=keyboard_reply)

@dp.message_handler()
async def check_rp(message: types.Message):
    if message.text == 'players':
        await message.reply(f"Tem ({len(allPlayers)}) jogando")
    elif message.text == '_button2':
        await message.answer(f"Hello, {(message.from_user.first_name)}!")
        # print(f"{gameCards.number} numero alterado")
    else:
        await message.reply(f"Your message is: {message.text}")
 
def addPlayer(name, username):
    allPlayers.append(Player(name, username, []))

executor.start_polling(dp)
