from aiogram import types, Dispatcher
from src.create_bot import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from src.databases import sql_database
from src.config import ADM_PASSWORD, STUDENT_PASSWORD, INTENSIVIST_PASSWORD
from src.handlers.admin import user_db
from src.keyboards.system_kb import keyboards_menu
from src.keyboards.inline_kb import city_markup, users_markup

count = 0


class Registration(StatesGroup):
    user_id = State()
    user_name = State()
    user_role = State()
    check_password = State()
    campus_name = State()





# @dp.message_handler(commands=["reg"], state=None)
async def cmd_reg(message: types.Message, state: FSMContext):
    """

    :type message: object
    """
    check = await user_db.check_registration(message.from_user.id)
    print(check)
    if not check:
        await Registration.first()
        async with state.proxy() as data:
            data['user_id'] = message.from_user.id
        await Registration.next()
        await bot.send_message(message.from_user.id, "Введите логин для авторизации!")
    else:
        await message.answer("Вы уже зарегистрированы!")


# @dp.message_handler(state="*", commands=["отмена"])
# @dp.message_handler(Text(equals='отмена', ignore_case=True), state="*")
async def cmd_cancel_registration(message: types.Message, state: FSMContext):
    # current_state = await state.get_state()
    # if current_state is None:
    #     return
    await state.finish()
    await message.reply('OK')


# @dp.message_handlers(state=Registration.user_id)
# async def user_answer_0(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data['user_id'] = message.from_user.id
#     await Registration.next()


# Ловим первый ответ от пользователя
# @dp.message_handler(state=Registration.user_name)
async def user_answer_1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user_name'] = message.text

        await Registration.next()
        await message.answer("Кто вы по жизни!", reply_markup=users_markup)


# Ловим второй ответ от птльзователя
# @dp.callback_query_handler(Text(startswith="user_"), state=Registration.user_role)
async def user_answer_2(callback: types.CallbackQuery, state: FSMContext):
    name = callback.data.split("_")[1]
    async with state.proxy() as data:
        data['user_role'] = name

        await Registration.next()
        await callback.message.answer("Ведите свой уникальный токен?")
        await callback.answer(f"Ваша роль {name}", show_alert=True)

# @dp.message_handlers(state=Registration.check_password)
async def check_password(message: types.Message, state: FSMContext):
    global count
    count += 1
    pasword = message.text
    data = await state.get_data()
    print(data)
    if pasword == ADM_PASSWORD and data['user_role'] == 'adm':
        await Registration.next()
        count = 0
        await message.answer("Из какого вы кампуса", reply_markup=city_markup)
    elif pasword == STUDENT_PASSWORD and data['user_role'] == 'student':
        await Registration.next()
        count = 0
        await message.answer("Из какого вы кампуса", reply_markup=city_markup)
    elif pasword == INTENSIVIST_PASSWORD and data['user_role'] == 'intensivist':
        await Registration.next()
        count = 0
        await message.answer("Из какого вы кампуса", reply_markup=city_markup)
    else:
        await message.answer("Неверный токен!!!")
        await message.answer("Попробуйте еще раз")
        await Registration.check_password.set()
        if count == 3:
            await message.answer("Попробуйте сначала")
            await state.finish()


# Ловим тертий ответ от пользователя
# @dp.callback_query_handler(Text(startswith="city_"), state=Registration.campus_name)
async def user_answer_3(callback: types.CallbackQuery, state: FSMContext):
    city = callback.data.split('_')[1]
    async with state.proxy() as data:
        data['campus_name'] = city
        # p = await state.get_data()
        # await message.answer(data)
        # await cmd_task()
    await user_db.sql_add_users(state)
    await callback.message.answer("Вы успешно зарегестрировались")
    await state.finish()


# @dp.message_handler(commands=["/double"])
async def cmd_double(message: types.Message):
    answer = await user_db.sql_check_booking("2022")
    await message.answer(answer)


# @dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):

    await bot.send_message(message.from_user.id, "Добро пожаловать!\nЭтот бот в разработке", reply_markup=keyboards_menu)
    await message.delete()


# @dp.message_handler()
async def cmd_task(message: types.Message):
    await message.answer("Введите токен для подтверждения роли!")
    if message.text == ADM_PASSWORD:
        await message.answer("Вы действительно адм")
    elif message.text == STUDENT_PASSWORD:
        await message.answer("Желаем удачи на проверках")
    elif message.text == INTENSIVIST_PASSWORD:
        await message.answer("Учи указатели дружок!")
    else:
        await message.answer("Пройдите регистрацию повторно")


# @dp.message_handlers(commands=["show"])
async def cmd_show(message: types.Message):
    read = await user_db.sql_output_all_users()
    await message.answer(*read)


# @dp.message_handler(commands=['my'])
async def cmd_my(message: types.Message):
    await user_db.sql_my_booking(message)


# @dp.message_handler(lambda message: "Помощь 🆘" in message.text)
async def cmd_help(message: types.Message):
    await message.answer(f"Дорогой друг это бот для бронирования /start")


# @dp.message_handler(lambda message: "Информация ⚠" in message.text)
async def cmd_information(message: types.Message):
    await message.answer("Ну что я могу сказать")


def register_handlers_system(dp : Dispatcher):
    dp.register_message_handler(cmd_start, commands=["start"])
    dp.register_message_handler(cmd_reg, lambda message: "Регистрация 🔐" in message.text, state=None)
    dp.register_message_handler(cmd_cancel_registration, state="*", commands=['отмена'])
    dp.register_message_handler(cmd_cancel_registration, Text(equals="отмена", ignore_case=True), state="*")
    # dp.register_message_handler(user_answer_0, state=Registration.user_id)
    dp.register_message_handler(user_answer_1, state=Registration.user_name)
    dp.register_callback_query_handler(user_answer_2, Text(startswith="user_"), state=Registration.user_role)
    dp.register_message_handler(check_password, state=Registration.check_password)
    dp.register_callback_query_handler(user_answer_3, Text(startswith="city_"), state=Registration.campus_name)
    dp.register_message_handler(cmd_show, commands=["show"])
    dp.register_message_handler(cmd_my, lambda message: "Мои брони 📝" in message.text)
    dp.register_message_handler(cmd_double, commands=['double'])
    dp.register_message_handler(cmd_help, lambda message: "Помощь 🆘" in message.text)
    dp.register_message_handler(cmd_information, lambda message: "Информация ⚠" in message.text)
