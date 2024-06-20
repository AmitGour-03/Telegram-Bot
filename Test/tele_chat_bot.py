# Almost same code written in: https://docs.aiogram.dev/en/latest/

import logging
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import os 

load_dotenv() # to load
API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher 
bot = Bot(token=API_TOKEN)   # it is for to pass the arguments so that it can perform based on this token

# # All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher(bot)  # description via hower

# code directly from above website link with little modification acc to below template in website
@dp.message_handler(commands=['start', 'help'])
async def command_start_handler(message: types.Message):
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    await message.reply(f"Hello,\nI am Apna Bot!\nPowered by aiogram.")


@dp.message_handler()
async def echo(message: types.Message):    # This is for jo bhi hum message karenge new_bot mai usi ko send kar do except '/start' and '/help'
    """
    This will return echo means same string as you will give.
    """
    await message.answer(message.text)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)


