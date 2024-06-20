import logging
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import os 
import openai
import asyncio

class Reference:
    """
    A class to store previous response from the chatgpt API
    """
    def __init__(self) -> None:
        self.response = ""

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

reference = Reference()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Model name
# as, we have different -different types of openai model
MODEL_NAME = "gpt-3.5-turbo"  # it is free 


# Initialize bot and dispatcher 
bot = Bot(token=TOKEN)   # it is for to pass the arguments so that it can perform based on this token

# # All handlers should be attached to the Router (or Dispatcher)
dispatcher = Dispatcher(bot)  # description via hower

def clear_past():
    """
    A function to clear the previous conservation and context
    """
    reference.response = ""

@dispatcher.message_handler(commands=['start'])
async def welcome(message: types.Message):
    """
    This handler receives messages with '/start' or '/help'
    """
    await message.reply("Hi,\nI am Apna Chat Bot!\nCreated by Dell Latitude. How can I assist you?")

@dispatcher.message_handler(commands=['clear'])
async def clear(message: types.Message):
    """
    A handler to clear the previous conversation and context
    """
    clear_past()
    await message.reply("I have cleared the past conversation and context")

@dispatcher.message_handler(commands=['help'])
async def help_command(message: types.Message):
    """
    A handler to display the help menu.
    """
    help_text = """
    Hi There, I'm ChatGPT based Telegram Bot created by Dell Latitude!\nPlease follow these commands:
    /start - to start the conversation
    /clear - to clear the past conversation
    /help - to get this help menu.
    I hope this helps. :)
    """
    await message.reply(help_text)

@dispatcher.message_handler()
async def handle_message(message: types.Message):
    """
    A handler to process the user's input and generate a response using ChatGPT API
    """
    print(f">>> USER: \n\t{message.text}")
    
    try:
        response = await openai.ChatCompletion.create(
            model=MODEL_NAME,
            messages=[
                {"role": "assistant", "content": reference.response}, 
                {"role": "user", "content": message.text}
            ]
        )
        reference.response = response.choices[0]['message']['content']
        print(f">>>ChatGPT: \n\t{reference.response}")
        await bot.send_message(chat_id=message.chat.id, text=reference.response)
        
    except openai.error.RateLimitError:
        await bot.send_message(chat_id=message.chat.id, text="Rate limit exceeded. Please try again later.")
        await asyncio.sleep(10)  # wait for some time before retrying

    except openai.error.OpenAIError as e:
        await bot.send_message(chat_id=message.chat.id, text=f"An error occurred: {str(e)}")

if __name__ == "__main__":
    executor.start_polling(dispatcher, skip_updates=False)

