from aiogram import types, Dispatcher
from bookbot21.src.create_bot import dp, bot
# from keyboards import *
# from database import sqlite_db


@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    # try:
    await bot.send_message(message.from_user.id, "Добро пожаловать!\nЭтот бот в разработке")
    await message.delete()
    # except:
    #     await message.reply("Общение с ботом только через кнопки")