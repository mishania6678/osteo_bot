import pymysql


class DBADMIN:
    def __init__(self):
        pass
        # self.blocked_hours = {}

    def add_chatid(self, username: str, chatid: int):
        self.__connect_database()

        with self.db.cursor() as cursor:
            cursor.execute(f'INSERT INTO `userinfo` (username, chatid) VALUES ("{username}", "{chatid}")')
            self.db.commit()

        self.__connect_database()

    def get_chatid(self, username: str) -> int:
        self.__connect_database()

        with self.db.cursor() as cursor:
            cursor.execute(f'SELECT chatid FROM `userinfo` WHERE username LIKE "%{username}"')
            chatid = cursor.fetchall()[0][0]

        self.__connect_database()

        return chatid

    # def add_blocked_hours(self, day: int, hours: list):
    #     self.__connect_database()
    #
    #     with self.db.cursor() as cursor:
    #         cursor.execute(f'SELECT list FROM `blocked_hours` WHERE id LIKE "%1"')
    #         self.blocked_hours = eval(cursor.fetchall()[0][0])
    #
    #     try:
    #         self.blocked_hours[day] = list(set(self.blocked_hours[day] + hours))
    #     except KeyError:
    #         self.blocked_hours[day] = hours
    #
    #     with self.db.cursor() as cursor:
    #         cursor.execute(f'UPDATE `blocked_hours` SET list = "{str(self.blocked_hours)}" WHERE id LIKE "%1"')
    #         self.db.commit()
    #
    #     self.__connect_database()
    #
    # def get_blocked_hours(self) -> dict:
    #     self.__connect_database()
    #
    #     with self.db.cursor() as cursor:
    #         cursor.execute(f'SELECT list from blocked_hours where id LIKE "%1"')
    #         blocked_hours = eval(cursor.fetchall()[0][0])
    #
    #     self.__connect_database()
    #
    #     return blocked_hours
    #
    # def unlock_hours(self, day: int, hours: list):
    #     self.__connect_database()
    #
    #     with self.db.cursor() as cursor:
    #         cursor.execute(f'SELECT list FROM `blocked_hours` WHERE id LIKE "%1"')
    #         self.blocked_hours = eval(cursor.fetchall()[0][0])
    #
    #     self.blocked_hours[day] = list(set(self.blocked_hours[day]) - set(hours))
    #
    #     with self.db.cursor() as cursor:
    #         cursor.execute(f'UPDATE `blocked_hours` SET list = "{str(self.blocked_hours)}" WHERE id LIKE "%1"')
    #         self.db.commit()
    #
    #     self.__connect_database()

    def __connect_database(self):
        self.db = pymysql.connect(
            host='eu-cdbr-west-03.cleardb.net',
            user='b83a46bc631fe8',
            password='f620966f',
            database='heroku_8b0a547625917b5'
        )

    def __close_database(self):
        self.db.close()

# db_admin = DBADMIN()
# db_admin.unlock_hours(21, ['17:00', '16:00', '12:00', '18:00', '15:00', '11:00', '19:00', '14:00', '10:00', '20:00', '13:00'])
