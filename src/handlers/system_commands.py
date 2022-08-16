from aiogram import types, Dispatcher
from bookbot21.src.create_bot import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from bookbot21.src.databases import sql_database
from bookbot21.src.config import ADM_PASSWORD, STUDENT_PASSWORD, INTENSIVIST_PASSWORD


class Registration(StatesGroup):
    user_name = State()
    user_role = State()
    campus_name = State()


# @dp.message_handler(commands=["reg"], state=None)
async def cmd_reg(message: types.Message):
    await bot.send_message(message.from_user.id, "Введите логин для авторизации!")
    await Registration.first()


#Ловим первый ответ от пользователя
# @dp.message_handler(state=Registration.user_name)
async def user_answer_1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user_name'] = message.text
        await Registration.next()
        await message.answer("Кто вы по жизни!")

# Ловим второй ответ от птльзователя
# @dp.message_handler(state=Registration.user_role)
async def user_answer_2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user_role'] = message.text
        await Registration.next()
        await message.answer("С какого вы кампуса?")

# Ловим тертий ответ от пользователя
# @dp.message_handler(state=Registration.campuse_name)
async def user_answer_3(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['campus_name'] = message.text
        p = await state.get_data()
        await message.answer(data)
        # await cmd_task()
        await message.answer("Вы успешно зарегестрировались")
        await state.finish()


# @dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await bot.send_message(message.from_user.id, "Добро пожаловать!\nЭтот бот в разработке")
    await message.delete()

# @dp.message_handler()
async def cmd_task(message: types.Message):
    await message.answer("Введите токен для подтверждения роли!")
    if message.text == ADM_PASSWORD:
        await message.answer("Вы действительно адм")
    elif message.text == STUDENT_PASSWORD:
        await message.answer("Желаем удачи  на проверках")
    elif message.text == INTENSIVIST_PASSWORD:
        await message.answer("Учи указатели дружок!")
    else:
        await message.answer("Пройдите регистрацию повторно")


def register_handlers_system(dp : Dispatcher):
    dp.register_message_handler(cmd_start, commands=["start"])
    dp.register_message_handler(cmd_reg, commands=["reg"], state=None)
    dp.register_message_handler(user_answer_1, state=Registration.user_name)
    dp.register_message_handler(user_answer_2, state=Registration.user_role)
    dp.register_message_handler(user_answer_3, state=Registration.campus_name)