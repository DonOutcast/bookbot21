from aiogram import Bot, Dispatcher, types
from prototype.kernel import config
from os.path import abspath
from aiogram.contrib.fsm_storage.memory import MemoryStorage # Позваляет хранить данные в оперативное памяти
# Для созранения ответтов от пользователя
storage = MemoryStorage()

# Инициализируем бота
bot = Bot(token=config.API_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
