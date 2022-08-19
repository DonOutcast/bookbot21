from aiogram.utils import executor
from create_bot import dp
from handlers import admin, system_commands, student


async def on_starttup(_):
    print("Бот запущен")


start_system = system_commands.BaseCommands(dp)
start_system.register_handlers_system()

start_admin = admin.Admin(dp)
start_admin.register_handlers_adm()

start_booking = student.Booking(dp)
start_booking.register_handlers_student()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_starttup)

