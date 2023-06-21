from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from calendar_admin import CalendarAdmin


class OsteoBotAdmin:
    def __init__(self):
        pass

    @staticmethod
    def main_kb():
        kb = ReplyKeyboardMarkup(row_width=3)
        kb.add(
            KeyboardButton(text='Записи на сьогодні 📅'),
            KeyboardButton(text='Записи на наступні декілька днів 📅'),
            KeyboardButton(text='Усі записи 📅'),
            KeyboardButton(text='Взяти вихідний 🥱'),
            KeyboardButton(text='Закрити час ❌')
        )

        return kb

    def calendar_kb(self, goal: str) -> InlineKeyboardMarkup:
        schedule = CalendarAdmin().available_time()

        days = []
        for d in schedule.keys():
            if schedule[d]:
                days.append(day)

        kb = InlineKeyboardMarkup(row_width=5)
        kb.add(*[InlineKeyboardButton(text=str(d), callback_data=f'day {goal} {d}') for d in days])

        return kb

    def time_schedule_kb(self, goal: str, day: int, name='') -> InlineKeyboardMarkup:
        hours = CalendarAdmin().available_time()[day]

        kb = InlineKeyboardMarkup(row_width=5)
        kb.add(*[InlineKeyboardButton(text=h, callback_data=f'{goal} {day} {h} {name}') for h in hours])

        return kb
