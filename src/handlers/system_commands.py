from aiogram.types import ContentType
from aiogram import types, Dispatcher
from src.create_bot import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from src.config import ADM_PASSWORD, STUDENT_PASSWORD, INTENSIVIST_PASSWORD
from src.databases.init_database import user_db
from src.keyboards.system_kb import keyboards_menu, back_menu_keyboard
from src.keyboards.inline_kb import city_markup, users_markup
from src.keyboards.inline_kb import filter_drop_booking


count = 0


class Registration(StatesGroup):
    user_id = State()
    user_name = State()
    user_role = State()
    check_password = State()
    campus_name = State()


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
        await bot.send_message(message.from_user.id, "Введите логин для авторизации!", reply_markup=back_menu_keyboard)
    else:
        await message.answer("Вы уже зарегистрированы!")


async def cmd_cancel_registration(message: types.Message, state: FSMContext):

    await message.delete()
    try:
        await bot.delete_message(message.from_user.id, message_id=message.message_id - 1)
    except:
        pass
    current_state = await state.get_state()
    if current_state is None:
        await message.answer('Вы вернулись в главное меню', reply_markup=keyboards_menu)
        return
    await state.finish()
    await message.answer('Вы вернулись в главное меню', reply_markup=keyboards_menu)


# Ловим первый ответ от пользователя
# @dp.message_handler(state=Registration.user_name)
async def user_answer_1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user_name'] = message.text
        await Registration.next()
        await message.answer("Кто вы по жизни!", reply_markup=users_markup)


async def check_choice_login(message: types.Message):
    await message.delete()
    await message.answer("Введите имя нормальным текстом!!!!!")


# Ловим второй ответ от птльзователя
# @dp.callback_query_handler(Text(startswith="user_"), state=Registration.user_role)
async def user_answer_2(callback: types.CallbackQuery, state: FSMContext):
    name = callback.data.split("_")[1]
    async with state.proxy() as data:
        data['user_role'] = name
    await Registration.next()
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=callback.message.text,
        reply_markup=None)
    name = output_warning(name)
    await callback.message.answer("Ведите свой уникальный токен: ")
    await callback.answer(f"Для подтверждения роли {name}, вам необходимо будет ввести токен", show_alert=True)


async def check_choice_role(message: types.Message):
    await message.delete()
    await message.answer("Я прошу тебя лишь  об одном нажми на кнопку")


# @dp.message_handler(state=Registration.user_role)
def output_warning(name_of_button) -> str:
    result = ""
    if name_of_button == 'adm':
        result = "Админа 🦁"
    elif name_of_button == 'student':
        result = "Студента "
    else:
        result = "Интенсивиста 🥷"
    return result


# @dp.message_handlers(state=Registration.check_password)
async def check_password(message: types.Message, state: FSMContext):
    global count
    if message.content_type != 'text':
        await message.answer("Введите свой токен просто токен!!!!!!")
        await Registration.check_password.set()
        await message.answer("Ведите свой уникальный токен: ")
    else:
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
    await user_db.sql_add_users(state)
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=callback.message.text,
        reply_markup=None)
    await callback.message.answer("Вы успешно зарегестрировались", reply_markup=keyboards_menu)
    await state.finish()


async def check_choice_city(message: types.Message):
    await message.delete()
    await message.answer("Я прошу тебя лишь  об одном нажми на кнопку")

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
    await message.answer(read)
    await user_db.sql_list_object("games")


# @dp.message_handler(commands=['my'])
async def cmd_my(message: types.Message):
    await user_db.sql_my_booking(message.from_user.id)


# @dp.callback_query_handler(filter_drop_booking.filter(action="bye_booking"))
async def delete_booking(callback: types.CallbackQuery, callback_data: dict):
    await user_db.sql_cancel_booking(callback_data['booking_id'])
    await callback.answer("Бронь успешно отменена ", show_alert=True)
    await callback.message.delete()


# @dp.message_handler(lambda message: "Помощь 🆘" in message.text)
async def cmd_help(message: types.Message):
    await message.answer(f"Дорогой друг это бот для бронирования /start")


# @dp.message_handler(lambda message: "Информация ⚠" in message.text)
async def cmd_information(message: types.Message):
    await message.answer("Ну что я могу сказать")


def register_handlers_system(dp : Dispatcher):
    dp.register_message_handler(cmd_start, commands=["start"])
    dp.register_message_handler(cmd_cancel_registration, Text(equals="Вернуться в главное меню 📜"), state="*")
    dp.register_message_handler(cmd_reg, lambda message: "Регистрация 🔐" in message.text, state=None)
    dp.register_message_handler(user_answer_1, state=Registration.user_name)
    dp.register_message_handler(check_choice_login, state=Registration.user_name, content_types=[ContentType.ANY])
    dp.register_callback_query_handler(user_answer_2, Text(startswith="user_"), state=Registration.user_role)
    dp.register_message_handler(check_choice_role, state=Registration.user_role, content_types=[ContentType.ANY])
    dp.register_message_handler(output_warning, state=Registration.user_role)
    dp.register_message_handler(check_password, state=Registration.check_password, content_types=[ContentType.ANY])
    dp.register_callback_query_handler(user_answer_3, Text(startswith="city_"), state=Registration.campus_name)
    dp.register_message_handler(check_choice_city, state=Registration.campus_name, content_types=[ContentType.ANY])
    dp.register_message_handler(cmd_show, commands=["show"])
    dp.register_message_handler(cmd_my, lambda message: "Мои брони 📝" in message.text)
    dp.register_message_handler(cmd_double, commands=['double'])
    dp.register_message_handler(cmd_help, lambda message: "Помощь 🆘" in message.text)
    dp.register_message_handler(cmd_information, lambda message: "Информация ⚠" in message.text)
    dp.register_callback_query_handler(delete_booking, filter_drop_booking.filter(action="bye_booking"))
