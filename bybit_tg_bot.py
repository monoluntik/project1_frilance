import requests
from aiogram import Bot, Dispatcher, executor, types
import asyncio
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ContentTypes, Message



API_TOKEN = '5662744006:AAF9OvgHAeJX1tTSL3yIkmIz0mKMJYVy5I8'

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Bybit Usernames"]
    keyboard.add(*buttons)
    await message.reply("Let's Go", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == "Bybit Usernames")
async def check_file(message: types.Message):
    await bot.send_document(message.from_user.id, open('bybit_usernames.txt', 'rb'))
    await message.reply("Откоректируйте указанный выше файл, и пришлите его сюда")

@dp.message_handler(content_types=ContentTypes.DOCUMENT)
async def doc_handler(message: Message):
    if document := message.document:
        await document.download(
            destination_dir="",
            destination_file="bybit_usernames.txt",
        )
        await message.reply("Новый файл успешно загружен")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
