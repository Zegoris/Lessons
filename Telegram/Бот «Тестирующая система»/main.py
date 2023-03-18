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
from buttons import inline_quest_m

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

statement, keyboard = {}, None

with open('questions.json', 'r') as file:
    data = json.load(file)
    data = data['test']

questions = [f"{i + 1}) {j['question']}" for i, j in enumerate(data)]
responses = [i['response'] for i in data]


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


async def new_user(message: types.Message):
    statement[message.from_user.id] = {'correct': 0, 'start': True, 'answer': False}


async def delete_keyboard():
    global keyboard
    try:
        if keyboard is not None:
            await keyboard.delete()
    except MessageToDeleteNotFound:
        pass


async def ender(message: types.Message):
    global keyboard
    await delete_keyboard()
    keyboard = await message.reply(f'Количество верных ответов: '
                                   f'{statement[message.from_user.id]["correct"]}\n'
                                   f'Хотите попробовать ещё раз?', reply_markup=inline_quest_m)


async def start(message: types.Message):
    await bot.send_message(message.from_user.id,
                           f"Привет, {message.from_user.full_name}! я - бот «Тестирующая система»\n"
                           f"Вы можете перезапустить бота, послав команду /stop.")
    await bot.send_message(message.from_user.id, '\n'.join(questions))


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
        statement[message.from_user.id]['answer'] = True


@dp.message_handler(commands=['stop'])
async def process_stop_command(message: types.Message):
    await bot.send_message(message.from_user.id, "Всего доброго!")
    await new_user(message)


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Это бот «Тестирующая система». "
                        "Введите команду /start для начала или /stop для перезапуска бота.\n"
                        "Отправь мне ответы каждый с новой строки без знаков препинания.")


@dp.callback_query_handler()
async def process_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    global keyboard
    await delete_keyboard()
    code = callback_query.data
    key = callback_query.from_user.id
    if code == 'command_yes':
        await bot.send_message(key, '\n'.join(questions))
    elif code == 'command_no':
        await bot.send_message(callback_query.from_user.id, "Всего доброго!")
        await new_user(callback_query)


@dp.message_handler()
async def prepare_answers(message: types.Message):
    try:
        if statement[message.from_user.id]['answer']:
            answers = message.text.split('\n')
            counter = 0
            for number, value in enumerate(answers):
                if value == responses[number]:
                    counter += 1
            statement[message.from_user.id]['correct'] = counter
            await ender(message)
    except KeyError:
        pass


if __name__ == '__main__':
    executor.start_polling(dp, on_shutdown=shutdown, skip_updates=True)