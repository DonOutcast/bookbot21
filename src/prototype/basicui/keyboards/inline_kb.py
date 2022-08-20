from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

city_markup = InlineKeyboardMarkup(row_width=1)
users_markup = InlineKeyboardMarkup(row_width=1)
objects_markup = InlineKeyboardMarkup(row_width=1)
name_rooms_markup = InlineKeyboardMarkup(row_width=1)

kzn_inline_button = InlineKeyboardButton(text="Казань 🏯", callback_data='city_kzn')
msk_inline_button = InlineKeyboardButton(text="Москва 🏭", callback_data='city_msk')
nsk_inline_button = InlineKeyboardButton(text="Новосибирск 🏰", callback_data='city_nsk')

city_markup.add(kzn_inline_button).add(msk_inline_button).add(nsk_inline_button)

adm_inline_button = InlineKeyboardButton(text="Адм 🦁", callback_data='user_adm')
student_inline_button = InlineKeyboardButton(text="Студент 👨‍💻", callback_data='user_student')
intensivist_inline_button = InlineKeyboardButton(text="Интенсивист 🥷", callback_data='user_intensivist')

users_markup.add(adm_inline_button).add(student_inline_button).add(intensivist_inline_button)


board_games_button = InlineKeyboardButton(text="Настольные игры 🎮 🎲♟", callback_data='object_Настольные игры')
conference_room_button = InlineKeyboardButton(text="Переговорные и конференц-залы 💼🕰", callback_data='object_Переговорные')
sports_equipment_button = InlineKeyboardButton(text="Спортивный инвентарь 🏀🏓🎯", callback_data='object_Спортивный инвентарь')
kitchen_room_button = InlineKeyboardButton(text="Кухни 🍽", callback_data="object_Кухня")
books_button = InlineKeyboardButton(text="Книги 📚", callback_data="object_Книги")
objects_markup.add(board_games_button).add(conference_room_button).add(sports_equipment_button).add(kitchen_room_button).add(books_button)

filter_drop_booking = CallbackData('drop', 'action', 'booking_id')


def create_button(booking_id: int) -> InlineKeyboardMarkup:

    cancle_booking = InlineKeyboardButton(text="Отменить бронь", callback_data=filter_drop_booking.new(action="bye_booking", booking_id=booking_id))
    cancel_markup = InlineKeyboardMarkup(row_width=1)
    cancel_markup.add(cancle_booking)
    return cancel_markup

#
# kzn_inline_button = InlineKeyboardButton(text=" 🏯", callback_data='city_kzn')
# msk_inline_button = InlineKeyboardButton(text="Москва 🏭", callback_data='city_msk')
# nsk_inline_button = InlineKeyboardButton(text="Новосибирск 🏰", callback_data='city_nsk')

# filter_list = CallbackData('type', 'action', 'id')


# async def type_list():
#     res = await user_db.sql_object_name()
#     return res
#
#
# async def object_list(type_name):
#     lis_of_type_name = await user_db.sql_list_object(type_name)
#     return lis_of_type_name


# def inline_type_list():
#     list_types = type_list()
#     row_button = []
#     for type_name in list_types:
#         line = InlineKeyboardButton(text=type_name,
#                                     callback_data=filter_list.new(action='get_type_list',
#                                                                   id=type_name))
#         row_button.append([line, ])
#     return InlineKeyboardMarkup(inline_keyboard=row_button)
#
#
# def inline_object_list(type_name):
#     list_object = object_list(type_name)
#     row_button = []
#     for object_id, object_name in list_object:
#         line = InlineKeyboardButton(text=object_name,
#                                     callback_data=filter_list.new(action='get_object_list',
#                                                                   id=object_id))
#         row_button.append([line, ])
#     return InlineKeyboardMarkup(inline_keyboard=row_button)



