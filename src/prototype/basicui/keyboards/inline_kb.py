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
claster_button = InlineKeyboardButton(text="Кластер ", callback_data="object_Kластер")
books_button = InlineKeyboardButton(text="Книги 📚", callback_data="object_Книги")
objects_markup.add(board_games_button).add(conference_room_button).add(sports_equipment_button).add(kitchen_room_button).add(books_button)

filter_drop_booking = CallbackData('drop', 'action', 'booking_id')


def create_button(booking_id: int) -> InlineKeyboardMarkup:

    cancle_booking = InlineKeyboardButton(text="Отменить бронь", callback_data=filter_drop_booking.new(action="bye_booking", booking_id=booking_id))
    cancel_markup = InlineKeyboardMarkup(row_width=1)
    cancel_markup.add(cancle_booking)
    return cancel_markup




