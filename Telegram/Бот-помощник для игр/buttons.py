from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

inline_btn_back = InlineKeyboardButton('Вернуться назад',
                                        callback_data='command_back')

inline_btn_close = InlineKeyboardButton('/close',
                                        callback_data='command_close')
inline_close_m = InlineKeyboardMarkup()
inline_close_m.add(inline_btn_close)

inline_btn_dice = InlineKeyboardButton('/dice', callback_data='command_dice')
inline_btn_timer = InlineKeyboardButton('/timer', callback_data='command_timer')
inline_start_m = InlineKeyboardMarkup()
inline_start_m.add(inline_btn_dice)
inline_start_m.add(inline_btn_timer)

inline_btn_6 = InlineKeyboardButton('Кинуть один шестигранный кубик',
                                    callback_data='command_6')
inline_btn_12 = InlineKeyboardButton('Кинуть 2 шестигранных кубика одновременно',
                                     callback_data='command_12')
inline_btn_20 = InlineKeyboardButton('Кинуть 20-гранный кубик',
                                     callback_data='command_20')
inline_dice_m = InlineKeyboardMarkup()
inline_dice_m.add(inline_btn_6)
inline_dice_m.add(inline_btn_12)
inline_dice_m.add(inline_btn_20)
inline_dice_m.add(inline_btn_back)

inline_btn_30 = InlineKeyboardButton('30 секунд',
                                    callback_data='command_30')
inline_btn_1 = InlineKeyboardButton('1 минута',
                                    callback_data='command_1')
inline_btn_5 = InlineKeyboardButton('5 минут',
                                    callback_data='command_5')
inline_timer_m = InlineKeyboardMarkup()
inline_timer_m.add(inline_btn_30)
inline_timer_m.add(inline_btn_1)
inline_timer_m.add(inline_btn_5)
inline_timer_m.add(inline_btn_back)
