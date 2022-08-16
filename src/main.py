from aiogram.utils import executor
from create_bot import dp
from handlers import admin, system_commands, intensivist, student
from databases import sql_database

async def on_starttup(_):
    print("Бот запущен")


system_commands.register_handlers_system(dp)
admin.register_handlers_adm(dp)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_starttup)

