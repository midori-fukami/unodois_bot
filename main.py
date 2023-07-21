import asyncio
import telegram
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ["BOT_TOKEN"]

async def main():
    bot = telegram.Bot(BOT_TOKEN)
    async with bot:
        await bot.send_message(text='Hi Midori!!!!', chat_id=307210099)

if __name__ == '__main__':
    asyncio.run(main())

    