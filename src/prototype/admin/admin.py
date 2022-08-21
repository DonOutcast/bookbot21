from aiogram import types
from aiogram.types import ContentType
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from prototype.kernel.create_bot import bot
from prototype.dal.databases.init_database import user_db
from aiogram.dispatcher.filters.state import State, StatesGroup
from prototype.basicui.keyboards.inline_kb import city_markup, objects_markup
from prototype.basicui.keyboards.system_kb import back_menu_keyboard, keyboards_menu


class AdmRoot(StatesGroup):
    name_for_object = State()
    type_for_object = State()
    description = State()
    campus_name = State()
    floor = State()
    number_of_room = State()
    photo = State()


class Admin:
    def __init__(self, dp):
        self.dp = dp

    @staticmethod
    async def cmd_add(message: types.Message):
        rule = await user_db.sql_check_rule(message.from_user.id)
        if rule is None:
            await message.answer("Зарегистрируйтесь!")
            await bot.send_sticker(message.from_user.id,
                                   sticker="CAACAgIAAxkBAAENm3Ni_0mPv0Bu4O7R2V62k81LaXzxNAACUAADQbVWDEsUyxvLOcdYKQQ")
        elif 'adm' in rule:
            await AdmRoot.first()
            await bot.send_sticker(message.from_user.id,
                                   sticker="CAACAgEAAxkBAAENoVljAh8xTOx1Nmxyk4ruq8V7cITCYQAC7AcAAuN4BAAB6DEEbU_xFOwpBA")
            await message.answer("Введите название объекта", reply_markup=back_menu_keyboard)
        else:
            await message.answer("Недостаточно прав! Обратитесь к ADM!")
            await bot.send_sticker(message.from_user.id,
                                   sticker="CAACAgIAAxkBAAENm2li_0kkz7kqFubgQ17PeKXTFxZmkQACRQADQbVWDB2S9JLvuNn8KQQ")

    @staticmethod
    async def adm_answer_1(message: types.Message, state: FSMContext):
        if len(message.text) > 20:
            await message.answer("Слишком длинное название\nНазвание не должно превышать двадцать символов")
            await AdmRoot.name_for_object.set()
        else:
            async with state.proxy() as data:
                await bot.send_sticker(message.from_user.id,
                                       sticker="CAACAgEAAxkBAAENoVljAh8xTOx1Nmxyk4ruq8V7cITCYQAC7AcAAuN4BAAB6DEEbU_xFOwpBA")
                data['name_for_object'] = message.text.capitalize()
                await AdmRoot.next()
                await message.answer("Введите тип объекта!", reply_markup=objects_markup)

    @staticmethod
    async def check_text_name_for_object(message: types.Message):
        if message.content_type != 'text':
            await message.delete()
            await message.answer("Введите название объекта текстом 📝!")
            await bot.send_sticker(message.from_user.id,
                                   sticker="CAACAgIAAxkBAAENm2di_0hRuQh_CEYY4vCtbwzpbMw_BQACcQgAAoSUQUlvaAkaprvOcykE")

    @staticmethod
    async def adm_answer_2(callback: types.CallbackQuery, state: FSMContext):
        object_after = callback.data.split('_')[1]
        async with state.proxy() as data:
            data['type_for_object'] = object_after
            await AdmRoot.next()
            await callback.answer()
            await callback.message.answer("Введите описание!")

    @staticmethod
    async def check_choice_type(message: types.Message):
        await message.delete()
        await message.answer("Я прошу лишь об одном просто выберите нужную вам кнопку!")
        await bot.send_sticker(message.from_user.id,
                               sticker="CAACAgIAAxkBAAENm1hi_0U1efcDilnmrARFOO3lRh36JAACmQcAAmMr4gmx63jV6i42GSkE")

    @staticmethod
    async def adm_answer_3(message: types.Message, state: FSMContext):
        await bot.send_sticker(message.from_user.id,
                               sticker="CAACAgEAAxkBAAENoVljAh8xTOx1Nmxyk4ruq8V7cITCYQAC7AcAAuN4BAAB6DEEbU_xFOwpBA")
        async with state.proxy() as data:
            data['description'] = message.text
            await AdmRoot.next()
            await message.answer("Выберите кампус!", reply_markup=city_markup)

    @staticmethod
    async def check_description(message: types.Message):
        await message.delete()
        await message.answer("Описание нужно написать текстом!")
        await bot.send_sticker(message.from_user.id,
                               sticker="CAACAgIAAxkBAAENm11i_0WUEosLLgLt0thPR5z5pRr3ggACoQcAAmMr4gm9FrBamSBazCkE")

    @staticmethod
    async def adm_answer_4(callback: types.CallbackQuery, state: FSMContext):
        city = callback.data.split('_')[1]
        async with state.proxy() as data:
            data['campus_name'] = city
            await AdmRoot.next()
            await callback.answer()
            await callback.message.answer("Введите этаж!")

    @staticmethod
    async def adm_answer_5(message: types.Message, state: FSMContext):
        cheking = message.text
        if cheking.isdigit():
            async with state.proxy() as data:
                data['floor'] = message.text
                await AdmRoot.next()
                await message.answer("Введите местоположение объекта!")
        else:
            await AdmRoot.floor.set()
            await message.answer("Введите этаж цифрами!")
            await bot.send_sticker(message.from_user.id,
                                   sticker="CAACAgIAAxkBAAENm11i_0WUEosLLgLt0thPR5z5pRr3ggACoQcAAmMr4gm9FrBamSBazCkE")

    @staticmethod
    async def check_choice_floor(message: types.Message):
        await message.delete()
        await message.answer("Номер этажа нужно прописать здесь числом")
        await bot.send_sticker(message.from_user.id,
                               sticker="CAACAgIAAxkBAAENm11i_0WUEosLLgLt0thPR5z5pRr3ggACoQcAAmMr4gm9FrBamSBazCkE")

    @staticmethod
    async def adm_answer_6(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['number_of_room'] = message.text
            await AdmRoot.next()
            await message.answer("Загрузите фото!")

    @staticmethod
    async def check_choice_room(message: types.Message):
        await message.delete()
        await message.answer("Название комнаты нужно прописать текстом")
        await bot.send_sticker(message.from_user.id,
                               sticker="CAACAgIAAxkBAAENm11i_0WUEosLLgLt0thPR5z5pRr3ggACoQcAAmMr4gm9FrBamSBazCkE")

    @staticmethod
    async def adm_answer_7(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await user_db.sql_add_objects(state)
        await message.answer("Вы успешно добавили объект!!!", reply_markup=keyboards_menu)
        await state.finish()

    @staticmethod
    async def check_download_photo(message: types.Message):
        await message.delete()
        await message.answer("Фотографию нужно загрузить из галереи")
        await bot.send_sticker(message.from_user.id,
                               sticker="CAACAgIAAxkBAAENm9Ri_2aFMnJj4vxwaLujBxQ8LYZzGQAChAIAAladvQpjOAcDbi3AuikE")

    def register_handlers_adm(self):
        self.dp.register_message_handler(self.cmd_add, lambda message: 'Добавить объект 👨🏻‍💻' in message.text, state=None)
        self.dp.register_message_handler(self.adm_answer_1, state=AdmRoot.name_for_object)
        self.dp.register_message_handler(self.check_text_name_for_object, state=[AdmRoot.name_for_object],
                                         content_types=[ContentType.ANY])
        self.dp.register_callback_query_handler(self.adm_answer_2, Text(startswith='object_'),
                                                state=AdmRoot.type_for_object)
        self.dp.register_message_handler(self.check_choice_type, state=[AdmRoot.type_for_object, AdmRoot.campus_name],
                                         content_types=[ContentType.ANY])
        self.dp.register_message_handler(self.adm_answer_3, state=AdmRoot.description)
        self.dp.register_message_handler(self.check_description, state=AdmRoot.description,
                                         content_types=[ContentType.ANY])
        self.dp.register_callback_query_handler(self.adm_answer_4, Text(startswith='city_'), state=AdmRoot.campus_name)
        self.dp.register_message_handler(self.adm_answer_5, state=AdmRoot.floor)
        self.dp.register_message_handler(self.check_choice_floor, state=AdmRoot.floor, content_types=[ContentType.ANY])
        self.dp.register_message_handler(self.adm_answer_6, state=AdmRoot.number_of_room)
        self.dp.register_message_handler(self.check_choice_room, state=AdmRoot.number_of_room,
                                         content_types=[ContentType.ANY])
        self.dp.register_message_handler(self.adm_answer_7, content_types=['photo'], state=AdmRoot.photo)
        self.dp.register_message_handler(self.check_download_photo, state=AdmRoot.photo,
                                         content_types=[ContentType.ANY])

