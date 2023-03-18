from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

inline_btn_yes = InlineKeyboardButton('Да',
                                     callback_data='command_yes')

inline_btn_no = InlineKeyboardButton('Нет',
                                     callback_data='command_no')
inline_quest_m = InlineKeyboardMarkup()
inline_quest_m.row(inline_btn_yes, inline_btn_no)
