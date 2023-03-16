from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils.exceptions import MessageToDeleteNotFound
from datetime import datetime
from random import randint
import asyncio

from config import TOKEN
from buttons import inline_start_m, inline_dice_m, inline_timer_m, inline_close_m

keyboard, dice, flag = None, None, True
list_dice = ['command_6', 'command_12', 'command_20']
list_timer = ['command_30', 'command_1', 'command_5']
list_special = ['command_back', 'command_close']

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


async def delete_keyboard():
    global keyboard
    try:
        if keyboard is not None:
            await keyboard.delete()
    except MessageToDeleteNotFound:
        pass


async def delete_message():
    global dice
    try:
        if dice is not None:
            await dice.delete()
    except MessageToDeleteNotFound:
        pass


async def timer(time):
    for seconds_left in range(time - 1, -1, -1):
        if flag:
            await asyncio.sleep(1)
        else:
            return False
    return True


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    global keyboard
    await delete_keyboard()
    keyboard = await bot.send_message(message.from_user.id,
                                      f"Привет, {message.from_user.full_name}! Я - твой бот-помощник для настольных игр.",
                                      reply_markup=inline_start_m)


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    global keyboard
    await delete_keyboard()
    keyboard = await message.reply("Этот бот предназначен для настольных игр.\n"
                                   "Вызовите одну из двух функций командой:",
                                   reply_markup=inline_start_m)


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'command_dice')
async def process_callback_dice(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    global keyboard
    await delete_keyboard()
    keyboard = await bot.send_message(callback_query.from_user.id, 'Выберите опцию...', reply_markup=inline_dice_m)


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'command_timer')
async def process_callback_timer(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    global keyboard
    await delete_keyboard()
    keyboard = await bot.send_message(callback_query.from_user.id,   'Выберите опцию...', reply_markup=inline_timer_m)


@dp.callback_query_handler(lambda callback_query: callback_query.data in list_special)
async def process_callback_special(callback_query: types.CallbackQuery):
    global keyboard, flag
    await delete_keyboard()
    code = callback_query.data
    if code == list_special[0]:
        await bot.answer_callback_query(callback_query.id)
        keyboard = await bot.send_message(callback_query.from_user.id,
                                          f"Привет, {callback_query.from_user.full_name}!"
                                          f" Я - твой бот-помощник для настольных игр.",
                                          reply_markup=inline_start_m)
    elif code == list_special[1]:
        await bot.answer_callback_query(callback_query.id)
        flag = False
        keyboard = await bot.send_message(callback_query.from_user.id, 'Выберите опцию...', reply_markup=inline_timer_m)


@dp.callback_query_handler(lambda callback_query: callback_query.data in list_dice)
async def process_callback_random(callback_query: types.CallbackQuery):
    global dice
    code = callback_query.data
    await delete_message()
    if code == list_dice[0]:
        await bot.answer_callback_query(callback_query.id)
        dice = await bot.send_message(callback_query.from_user.id, f'{randint(1, 6)}')
    elif code == list_dice[1]:
        await bot.answer_callback_query(callback_query.id)
        dice = await bot.send_message(callback_query.from_user.id, f'{randint(1, 6)} {randint(1, 6)}')
    elif code == list_dice[2]:
        await bot.answer_callback_query(callback_query.id)
        dice = await bot.send_message(callback_query.from_user.id, f'{randint(1, 20)}')


@dp.callback_query_handler(lambda callback_query: callback_query.data in list_timer)
async def process_callback_time(callback_query: types.CallbackQuery):
    global keyboard, flag
    await delete_keyboard()
    code = callback_query.data
    flag = True
    if code == list_timer[0]:
        await bot.answer_callback_query(callback_query.id)
        keyboard = await bot.send_message(callback_query.from_user.id,
                                          f'Засек 30 сек', reply_markup=inline_close_m)
        if await timer(int(0.5 * 60)):
            await delete_keyboard()
            keyboard = await bot.send_message(callback_query.from_user.id,
                                              f'30 сек истекло', reply_markup=inline_timer_m)
    elif code == list_timer[1]:
        await bot.answer_callback_query(callback_query.id)
        keyboard = await bot.send_message(callback_query.from_user.id,
                                          f'Засек 1 минуту', reply_markup=inline_close_m)
        if await timer(1 * 60):
            await delete_keyboard()
            keyboard = await bot.send_message(callback_query.from_user.id,
                                              f'1 минута истекла', reply_markup=inline_timer_m)
    elif code == list_timer[2]:
        await bot.answer_callback_query(callback_query.id)
        keyboard = await bot.send_message(callback_query.from_user.id,
                                          f'Засек 5 минут', reply_markup=inline_close_m)
        if await timer(5 * 60):
            await delete_keyboard()
            keyboard = await bot.send_message(callback_query.from_user.id,
                                              f'5 минут истекло', reply_markup=inline_timer_m)



if __name__ == '__main__':
    executor.start_polling(dp, on_shutdown=shutdown, skip_updates=True)