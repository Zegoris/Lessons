from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

inline_btn_hall = InlineKeyboardButton('Холл',
                                     callback_data='command_hall')

inline_btn_sculpt = InlineKeyboardButton('Зал скульптур',
                                     callback_data='command_sculpt')
inline_btn_image = InlineKeyboardButton('Зал картин',
                                     callback_data='command_image')
inline_btn_pants = InlineKeyboardButton('Зал нижнего белья',
                                     callback_data='command_pants')
inline_hall_m = InlineKeyboardMarkup()
inline_hall_m.add(inline_btn_sculpt)

inline_sculpt_m = InlineKeyboardMarkup()
inline_sculpt_m.add(inline_btn_image)

inline_image_m = InlineKeyboardMarkup()
inline_image_m.add(inline_btn_pants)
inline_image_m.add(inline_btn_hall)

inline_pants_m = InlineKeyboardMarkup()
inline_pants_m.add(inline_btn_hall)

inline_btn_yes = InlineKeyboardButton('Да',
                                     callback_data='command_yes')

inline_btn_no = InlineKeyboardButton('Нет',
                                     callback_data='command_no')
inline_choose_m = InlineKeyboardMarkup()
inline_choose_m.row(inline_btn_yes, inline_btn_no)