from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

inline_btn_en = InlineKeyboardButton('Русский - Английский',
                                     callback_data='command_en')

inline_btn_ru = InlineKeyboardButton('Английский - Русский',
                                     callback_data='command_ru')
inline_language_m = InlineKeyboardMarkup()
inline_language_m.add(inline_btn_ru)
inline_language_m.add(inline_btn_en)
