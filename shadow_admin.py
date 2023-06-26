import asyncio

import os
from calendar_admin import CalendarAdmin
from db_admin import DBADMIN

from aiogram import Bot

from datetime import date
import time

db_admin = DBADMIN()


class ShadowAdmin(CalendarAdmin):
    def remove_ended_sessions(self):
        while True:
            sessions = self.get_data()
            for s in sessions:
                year, month, day, hour = int(s[1][:4]), int(s[1][5:7]), int(s[1][8:10]), s[1][11:16]
                if year < date.today().year or (year >= date.today().year and month < date.today().month) or \
                        (year >= date.today().year and month >= date.today().month and day < date.today().day):
                    self.cancel_session(day=day, hour=hour)

            time.sleep(21600)

    def check_nearest_sessions(self):
        async def remind(chatid: int, hour: str):
            bot = Bot(os.environ.get('BOT_TOKEN'))
            await bot.send_message(chat_id=chatid, text=f'❗ НАГАДУВАННЯ: у Вас заплановано сеанс на {hour}')

        while True:
            for s in self.get_data():
                day, hour = int(s[1][8:10]), s[1][11:16]
                if day == date.today().day + 3:
                    asyncio.run(remind(chatid=db_admin.get_chatid(username=s[0]), hour=hour))

            time.sleep(86400)
