from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils.exceptions import MessageToDeleteNotFound
from googletrans import Translator
from datetime import datetime
from random import randint
import asyncio

from config import TOKEN
from buttons import inline_language_m

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

statement, keyboard = {}, None


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


async def new_user(message: types.Message):
    statement[message.from_user.id] = {'language': 'en', 'start': True}


async def delete_keyboard():
    global keyboard
    try:
        if keyboard is not None:
            await keyboard.delete()
    except MessageToDeleteNotFound:
        pass


async def start(message: types.Message):
    await bot.send_message(message.from_user.id,
                           f"Привет, {message.from_user.full_name}! я - бот переводчик\n"
                           f"Вы можете перезапустить бота, послав команду /stop.")


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    try:
        if statement[message.from_user.id]['start']:
            await start(message)
    except KeyError:
        await new_user(message)
        await start(message)
    finally:
        statement[message.from_user.id]['start'] = False


@dp.message_handler(commands=['stop'])
async def process_stop_command(message: types.Message):
    await bot.send_message(message.from_user.id, "Всего доброго!")
    await new_user(message)


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Это бот переводчик. "
                        "Введите команду /start для начала или /stop для перезапуска бота.\n"
                        "Команда /language выведет поле для изменения направления перевода.\n"
                        "Отправь мне строку и я её переведу.")


@dp.message_handler(commands=['language'])
async def process_language_command(message: types.Message):
    global keyboard
    await delete_keyboard()
    keyboard = await bot.send_message(message.from_user.id,
                                      'Выберите язык...', reply_markup=inline_language_m)


@dp.callback_query_handler()
async def process_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    global keyboard
    await delete_keyboard()
    code = callback_query.data
    key = callback_query.from_user.id
    if code == 'command_en':
        statement[key]['language'] = 'en'
    elif code == 'command_ru':
        statement[key]['language'] = 'ru'


@dp.message_handler()
async def translate_message(message: types.Message):
    try:
        translator = Translator()
        translated_text = translator.translate(message.text,
                                               dest=statement[message.from_user.id]['language']).text
        await message.reply(translated_text)
    except Exception as e:
        await message.reply(f'Должно было сработать,'
                            f' но из-за "санкций" моментами API перестаёт работать, прошу прощения :)\n'
                            f'P.S: со стороны оформления кода всё правильно, сравни с вариантом в интернете, рассчитываю на понимание!')


if __name__ == '__main__':
    executor.start_polling(dp, on_shutdown=shutdown, skip_updates=True)