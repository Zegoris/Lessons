from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils.exceptions import MessageToDeleteNotFound
from googletrans import Translator
from datetime import datetime
from random import randint
import json

from config import TOKEN
from buttons import inline_hall_m, inline_sculpt_m, inline_image_m, inline_pants_m, inline_choose_m

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

statement, keyboard = {}, None

first_room, second_room, third_room, fourth_room, hall_room = ['command_sculpt'], ['command_image'],\
    ['command_hall', 'command_pants'], ['command_hall'], ['command_yes','command_no']


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


async def new_user(message: types.Message):
    statement[message.from_user.id] = {'start': True}


async def delete_keyboard():
    global keyboard
    try:
        if keyboard is not None:
            await keyboard.delete()
    except MessageToDeleteNotFound:
        pass


async def start(message: types.Message):
    global keyboard
    await delete_keyboard()
    await bot.send_message(message.from_user.id,
                           f"Привет, {message.from_user.full_name}! Я - бот путеводитель.\n"
                           f"Приветствую вас в музее античности! "
                           f"Вы можете перезапустить бота, послав команду /stop.")
    keyboard = await bot.send_message(message.from_user.id,
                                      'Добро пожаловать! Пожалуйста, сдайте верхнюю одежду в гардероб! '
                                      'Пройдёмте в следующий зал.', reply_markup=inline_hall_m)


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
    global keyboard
    await delete_keyboard()
    keyboard = await bot.send_message(message.from_user.id, "Всего доброго!")
    await new_user(message)


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Это бот путеводитель. "
                        "Введите команду /start для начала или /stop для перезапуска бота.\n")


@dp.callback_query_handler(lambda callback_query: callback_query.data in first_room)
async def process_callback_first(callback_query: types.CallbackQuery):
    global keyboard
    await delete_keyboard()
    await bot.answer_callback_query(callback_query.id)
    keyboard = await bot.send_message(callback_query.from_user.id,
                                      'В данном зале представлены скульптуры античности. Пройдёмте в следующий зал.',
                                      reply_markup=inline_sculpt_m)


@dp.callback_query_handler(lambda callback_query: callback_query.data in second_room)
async def process_callback_second(callback_query: types.CallbackQuery):
    global keyboard
    await delete_keyboard()
    await bot.answer_callback_query(callback_query.id)
    keyboard = await bot.send_message(callback_query.from_user.id,
                                      'В данном зале представлены картины античности. Пройдёмте в следующий зал.',
                                      reply_markup=inline_image_m)


@dp.callback_query_handler(lambda callback_query: callback_query.data in second_room)
async def process_callback_second(callback_query: types.CallbackQuery):
    global keyboard
    await delete_keyboard()
    await bot.answer_callback_query(callback_query.id)
    keyboard = await bot.send_message(callback_query.from_user.id,
                                      'В данном зале представлены картины античности. Пройдёмте в следующий зал.',
                                      reply_markup=inline_image_m)


@dp.callback_query_handler(lambda callback_query: callback_query.data in third_room)
async def process_callback_third(callback_query: types.CallbackQuery):
    global keyboard
    await delete_keyboard()
    code = callback_query.data
    await bot.answer_callback_query(callback_query.id)
    if code == third_room[0]:
        keyboard = await bot.send_message(callback_query.from_user.id,
                                          'Добро пожаловать в холл. Хотите покинуть музей?',
                                          reply_markup=inline_choose_m)
    elif code == third_room[1]:
        keyboard = await bot.send_message(callback_query.from_user.id,
                                          'В данном зале представлены нижнее бельё античности. Пройдёмте в следующий зал.',
                                          reply_markup=inline_pants_m)


@dp.callback_query_handler(lambda callback_query: callback_query.data in fourth_room)
async def process_callback_second(callback_query: types.CallbackQuery):
    global keyboard
    await delete_keyboard()
    await bot.answer_callback_query(callback_query.id)
    keyboard = await bot.send_message(callback_query.from_user.id,
                                      'Добро пожаловать в холл. Хотите покинуть музей?',
                                      reply_markup=inline_choose_m)


@dp.callback_query_handler(lambda callback_query: callback_query.data in hall_room)
async def process_callback_third(callback_query: types.CallbackQuery):
    global keyboard
    await delete_keyboard()
    code = callback_query.data
    await bot.answer_callback_query(callback_query.id)
    if code == hall_room[0]:
        await bot.send_message(callback_query.from_user.id,
                               'Всего доброго, не забудьте забрать верхнюю одежду в гардеробе!')
        await new_user(callback_query)
    elif code == hall_room[1]:
        keyboard = await bot.send_message(callback_query.from_user.id,
                                          'Хорошо, давайте продолжим нашу экскурсию.',
                                          reply_markup=inline_hall_m)


if __name__ == '__main__':
    executor.start_polling(dp, on_shutdown=shutdown, skip_updates=True)