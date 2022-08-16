from aiogram import Bot, Dispatcher
import config

# Инициализируем бота
bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)
