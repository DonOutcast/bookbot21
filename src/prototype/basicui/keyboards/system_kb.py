from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, WebAppInfo

help_button = KeyboardButton("О себе 🆘")
information_button = KeyboardButton('Информация ⚠️')
registration_button = KeyboardButton('Регистрация 🔐')
booking_button = KeyboardButton('Бронирование ✅')
my_bookings_button = KeyboardButton('Мои брони 📝')
admin_button = KeyboardButton('Добавить объект 👨🏻‍💻')
keyboards_menu = ReplyKeyboardMarkup(resize_keyboard=True)


back_to_menu_button = KeyboardButton("Вернуться в главное меню 📜")
back_menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
back_menu_keyboard.add(back_to_menu_button)

web_app = WebAppInfo(url="https://donoutcast.github.io/")
site_button = KeyboardButton(text="Site", web_app=web_app)
keyboards_menu.row(registration_button, admin_button).row(booking_button, my_bookings_button).row(help_button, information_button).add(site_button)


catch_keyboards = ReplyKeyboardMarkup(resize_keyboard=True)
catch_keyboards.add(site_button)
