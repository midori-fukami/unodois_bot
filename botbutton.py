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

isStarted = False

isNew = False

keyboard_reply = ReplyKeyboardMarkup(
	resize_keyboard=True, one_time_keyboard=True).add("new", "start")

@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    await message.reply("Hello! how are you?", reply_markup=keyboard_reply)

@dp.message_handler(commands=['join'])
async def join(message: types.Message):
    if isNew is False:
        await message.reply(f"No game is running at the moment. Create a new game with /new", reply_markup=keyboard_reply)
        print(f"No game is running at the moment. Create a new game with /new")

    aux = []
    for x in allPlayers:
        aux.append(x.username)

    if message.from_user.username in aux:
        await message.reply(f"{message.from_user.username} already joined the game", reply_markup=keyboard_reply)
        print(f"{message.from_user.username} already joined the game")
    else:
        addPlayer(message.from_user.first_name, message.from_user.username)
        await message.reply(f"@{message.from_user.username} joined the game", reply_markup=keyboard_reply)
        print(f"{message.from_user.username} joined the game")

@dp.message_handler()
async def check_rp(message: types.Message):
    global isNew
    if message.text == 'new':
        if not isNew:            
            isNew = True
            await message.reply("Created a new game! Join with /join and start with /start", reply_markup=keyboard_reply)
            print("Created a new game! Join with /join and start with /start")
        else:
            await message.reply("There is already a game running in this chat. Join with /join", reply_markup=keyboard_reply)
            print("There is already a game running in this chat. Join with /join")
    elif message.text == 'start':
        global isStarted
        if isNew and not isStarted:
            isStarted = True
            await message.reply("First player...(nome do primeiro)", reply_markup=keyboard_reply)
        elif isStarted:
            await message.reply("The game has already started", reply_markup=keyboard_reply)
        elif not isNew:
            await message.reply(f"Not playing right now. Use /new to start a game")

        await message.reply(f"Tem ({len(allPlayers)}) jogando")
        print(f"Tem ({len(allPlayers)}) jogando")
    else:
        await message.reply(f"Not playing right now. Use /new to start a game or /join to join the current game", reply_markup=keyboard_reply)
 #5904849719 escolher cor
# @dp.message_handler()
@dp.message_handler(content_types=types.ContentType.STICKER)
async def check_st(message: types.Message):
    await message.reply(f"something not a message", reply_markup=keyboard_reply)
    await message.reply(f"{message}", reply_markup=keyboard_reply)
    print(f"sticker: ({message})")
    

def addPlayer(name, username):
    allPlayers.append(Player(name, username, []))

executor.start_polling(dp)

AgADrg4AAvX2mVE

AgAD6A8AAn_ckVE