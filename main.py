from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from osteo_bot_admin import OsteoBotAdmin
from calendar_admin import CalendarAdmin
from shadow_admin import ShadowAdmin
from db_admin import DBADMIN

import threading

bot = Bot('6273403006:AAGhCvbGqkpFTO_XEihqolz8u82khxmjqLk')
dp = Dispatcher(bot)

osteo_bot_admin = OsteoBotAdmin()
calendar_admin = CalendarAdmin()
shadow_admin = ShadowAdmin()
db_admin = DBADMIN()

blocked_hours = {}
# vars for rescheduling
old_day, old_hour, name = 0, '', ''


@dp.message_handler(commands=['start'])
async def start_handler(msg: types.Message):
    if msg.from_user.username == 'wargkul':
        threading.Thread(target=shadow_admin.remove_ended_sessions).start()
        threading.Thread(target=shadow_admin.check_nearest_sessions).start()
        # threading.Thread(target=shadow_admin.unlock_hours_controller).start()

        await bot.send_message(chat_id=msg.chat.id, text='Ласкаво прошу, Валентине! 😉', reply_markup=osteo_bot_admin.main_kb())

    else:
        await bot.send_message(chat_id=msg.chat.id, text='Доступ заборонено ⚠')


@dp.message_handler(content_types=['text'])
async def text_handler(msg: types.Message):
    if msg.from_user.username == 'wargkul':
        if msg.text in ('Записи на сьогодні 📅', 'Записи на наступні декілька днів 📅', 'Усі записи 📅'):
            range_map = {'Записи на сьогодні 📅': 'today', 'Записи на наступні декілька днів 📅': 'week',  'Усі записи 📅': 'all'}
            if calendar_admin.show_sessions_rooted(range_=range_map[msg.text]) in ('None', {}):
                await bot.send_message(chat_id=msg.chat.id, text='Сеансів не заплановано 😴')
            else:
                for s_d, s_t in calendar_admin.show_sessions_rooted(range_=range_map[msg.text]).items():
                    for t, n in s_t:
                        delete_kb = InlineKeyboardMarkup(row_width=1).add(
                            InlineKeyboardButton(text='Скасувати сеанс ❌', callback_data=f'ses del {s_d} {t}'),
                            InlineKeyboardButton(text='Перенести сеанс ✏️', callback_data=f'ses edit {s_d} {t} {n}')
                        )
                        await bot.send_message(chat_id=msg.chat.id, text=f'{s_d}: {t}', reply_markup=delete_kb)

        elif msg.text == 'Взяти вихідний 🥱':
            await bot.send_message(chat_id=msg.chat.id, text='Виберіть день 🔀',
                                   reply_markup=osteo_bot_admin.calendar_kb(goal='blockd'))

        elif msg.text == 'Закрити час ❌':
            await bot.send_message(chat_id=msg.chat.id, text='Виберіть день 🔀',
                                   reply_markup=osteo_bot_admin.calendar_kb(goal='seld'))

    else:
        await bot.send_message(chat_id=msg.chat.id, text='Доступ заборонено ⚠')


@dp.callback_query_handler(lambda c: c.data and (c.data.startswith('seld') or c.data.startswith('selboth') or c.data.startswith('blockd')))
async def calendar_keyboard_callback_data_handler(call: types.CallbackQuery):
    global blocked_hours

    if call.data.startswith('seld'):
        await bot.send_message(chat_id=call.message.chat.id, text='Виберіть час, який хочете заблокувати 🔀',
                               reply_markup=osteo_bot_admin.time_schedule_kb(goal='blockh', day=int(call.data.split()[1])))

    elif call.data.startswith('selboth'):
        await bot.send_message(chat_id=call.message.chat.id, text='Виберіть новий час 🔀',
                               reply_markup=osteo_bot_admin.time_schedule_kb(goal='selh', day=int(call.data.split()[1])))

    else:
        for h in ['10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00']:
            calendar_admin.schedule_session(name='blocked', day=int(call.data.split()[1]), hour=h)
        await bot.send_message(chat_id=call.message.chat.id, text='День заблоковано ✅')


@dp.callback_query_handler(lambda c: c.data and (c.data.startswith('selh') or c.data.startswith('blockh')))
async def time_schedule_keyboard_callback_data_handler(call: types.CallbackQuery):
    global blocked_hours

    if call.data.startswith('selh'):
        calendar_admin.reschedule_session(name=name, old_day=old_day, old_hour=old_hour,
                                          new_day=int(call.data.split()[1]), new_hour=call.data.split()[2])
        await bot.send_message(chat_id=call.message.chat.id, text='Час сеансу змінено ✅')

    else:
        calendar_admin.schedule_session(name='blocked', day=int(call.data.split()[1]), hour=call.data.split()[2])
        await bot.send_message(chat_id=call.message.chat.id, text='Час заблоковано ✅')


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('ses'))
async def sessions_keyboard_callback_data_handler(call: types.CallbackQuery):
    global old_day, old_hour, name

    if call.data.split()[1] == 'del':
        calendar_admin.cancel_session(day=int(call.data.split()[2].split('.')[0]), hour=call.data.split()[3])
        await bot.send_message(chat_id=call.message.chat.id, text='Сеанс скасовано ✅')

    else:
        old_day, old_hour, name = int(call.data.split()[2].split('.')[0]), call.data.split()[3], call.data.split()[4]
        await bot.send_message(chat_id=call.message.chat.id, text='Виберіть новий день 🔀',
                               reply_markup=osteo_bot_admin.calendar_kb(goal='selboth'))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
