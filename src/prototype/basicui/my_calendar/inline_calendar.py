from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from datetime import datetime
from dateutil.relativedelta import relativedelta
from calendar import monthrange

filter_list_date = CallbackData('calendar', 'type', 'date')


async def get_date(date=None) -> InlineKeyboardMarkup:
    cal_dict = {1: 'Январь',
                2: 'Февраль',
                3: 'Март',
                4: 'Апрель',
                5: 'Май',
                6: 'Июнь',
                7: 'Июль',
                8: 'Август',
                9: 'Сентябрь',
                10: 'Октябрь',
                11: 'Ноябрь',
                12: 'Декабрь'
                }

    if date is None:
        dt = datetime.now()
        date = dt.strftime("%Y/%m")
    dt = datetime.strptime(date, "%Y/%m")

    line_year = [
        InlineKeyboardButton(text='<',
                             callback_data=filter_list_date.new(type='refresh',
                                                                date=(dt - relativedelta(years=1)).strftime("%Y/%m"))),

        InlineKeyboardButton(text=str(dt.year),
                             callback_data=str(dt.year)),

        InlineKeyboardButton(text='>',
                             callback_data=filter_list_date.new(type='refresh',
                                                                date=(dt + relativedelta(years=1)).strftime("%Y/%m"))),
    ]

    line_mounth = [
        InlineKeyboardButton(text='<',
                             callback_data=filter_list_date.new(type='refresh',
                                                                date=(dt - relativedelta(months=1)).strftime("%Y/%m"))),

        InlineKeyboardButton(text=cal_dict[dt.month],
                             callback_data=str(dt.month)),

        InlineKeyboardButton(text='>',
                             callback_data=filter_list_date.new(type='refresh',
                                                                date=(dt + relativedelta(months=1)).strftime("%Y/%m"))),
    ]

    first_day = dt.weekday()
    count_days = monthrange(dt.year, dt.month)[1]
    res_list_inline_but = [line_year, line_mounth]

    line = []
    for num_day in range(7 * 6):
        if num_day < first_day or num_day > count_days + first_day - 1:
            line.append(InlineKeyboardButton(text='_', callback_data='_'))
        else:
            day = num_day - first_day + 1
            mount = dt.month
            year = dt.year
            line.append(InlineKeyboardButton(text=str(day),
                                             callback_data=filter_list_date.new(type='get_date',
                                                                                date=f'{day}/{mount}/{year}')))
        if len(line) == 7:
            res_list_inline_but.append(line)
            line = []

    res_list_inline_but.append([InlineKeyboardButton(text='Отмена',
                                callback_data='cancel_calendar'),])

    return InlineKeyboardMarkup(inline_keyboard=res_list_inline_but)
