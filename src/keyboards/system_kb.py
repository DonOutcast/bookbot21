from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
# from aiogram.types import *

help_button = KeyboardButton("Помощь 🆘")
information_button = KeyboardButton('Информация ⚠️')
registration_button = KeyboardButton('Регистрация 🔐')
booking_button = KeyboardButton('Бронирование ✅')
my_bookings_button = KeyboardButton('Мои брони 📝')
admin_button = KeyboardButton('Добавление 👨🏻‍💻')
keyboards_menu = ReplyKeyboardMarkup(resize_keyboard=True)


back_to_menu_button = KeyboardButton("Вернуться в главное меню 📜")
back_menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
back_menu_keyboard.add(back_to_menu_button)

keyboards_menu.row(registration_button, admin_button).row(booking_button, my_bookings_button).row(help_button, information_button)
