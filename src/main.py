from aiogram.utils import executor
from create_bot import dp
from handlers import admin, system_commands


async def on_starttup(_):
    print("Бот запущен")

if __name__ == "__main__":
    admin.start()
    system_commands.cmd_start()
    executor.start_polling(dp, skip_updates=True, on_startup=on_starttup)
