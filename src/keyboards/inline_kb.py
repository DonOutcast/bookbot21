from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


city_markup = InlineKeyboardMarkup(row_width=1)
users_markup = InlineKeyboardMarkup(row_width=1)
objects_markup = InlineKeyboardMarkup(row_width=1)


kzn_inline_button = InlineKeyboardButton(text="Казань 🏯​", callback_data='city_kzn')
msk_inline_button = InlineKeyboardButton(text="Москва 🏭​", callback_data='city_msk')
nsk_inline_button = InlineKeyboardButton(text="Новосибирск ​🏰​", callback_data='city_nsk')

city_markup.add(kzn_inline_button).add(msk_inline_button).add(nsk_inline_button)

adm_inline_button = InlineKeyboardButton(text="Адм 🦁​", callback_data='user_adm')
student_inline_button = InlineKeyboardButton(text="Студент ​👨‍💻​", callback_data='user_student')
intensivist_inline_button = InlineKeyboardButton(text="Интенсивист 🥷​", callback_data='user_intensivist')

users_markup.add(adm_inline_button).add(student_inline_button).add(intensivist_inline_button)


board_games_button = InlineKeyboardButton(text="Настольные игры ", callback_data='object_games')
conference_room_button = InlineKeyboardButton(text="Переговорная ", callback_data='object_conference')
sports_equipment_button = InlineKeyboardButton(text="Спортивный инвентарь", callback_data='object_sports')
kitchen_room_button = InlineKeyboardButton(text="Кухня ", callback_data="object_kitchen")

objects_markup.add(board_games_button).add(conference_room_button).add(sports_equipment_button).add(kitchen_room_button)
