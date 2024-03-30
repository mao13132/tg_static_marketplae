import datetime
import sqlite3
from datetime import datetime

from src.logger._logger import logger_msg


class BotDB:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    def __init__(self, db_file):
        try:

            self.conn = sqlite3.connect(db_file, timeout=30)
            print('Подключился к SQL DB:', db_file)
            self.cursor = self.conn.cursor()
            self.check_table()
        except Exception as es:
            print(f'Ошибка при работе с SQL {es}')

    def check_table(self):

        try:
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS "
                                f"users (id_pk INTEGER PRIMARY KEY AUTOINCREMENT, "
                                f"id_user TEXT, "
                                f"login TEXT, "
                                f"join_date DATETIME, "
                                f"last_time DATETIME DEFAULT 0, "
                                f"push1 BOOLEAN DEFAULT 1, "
                                f"other TEXT)")

        except Exception as es:
            print(f'SQL исключение check_table users {es}')

        try:
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS "
                                f"statistic (id_pk INTEGER PRIMARY KEY AUTOINCREMENT, "
                                f"marketplace TEXT, "
                                f"brand TEXT, "
                                f"orders NUMERIC, "
                                f"profit FLOAT, "
                                f"date DATETIME, "
                                f"other TEXT)")

        except Exception as es:
            print(f'SQL исключение check_table statistic {es}')

    def check_or_add_user(self, id_user, login):

        result = self.cursor.execute(f"SELECT * FROM users WHERE id_user='{id_user}'")

        response = result.fetchall()

        if not response:
            now_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            self.cursor.execute("INSERT OR IGNORE INTO users ('id_user', 'login',"
                                "'join_date') VALUES (?,?,?)",
                                (id_user, login,
                                 now_date,))

            self.conn.commit()

            return True

        return False

    def check_or_add_static(self, sql_data):

        try:

            result = self.cursor.execute(f"SELECT * FROM statistic WHERE date='{sql_data['date']}' and "
                                         f"marketplace='{sql_data['marketplace']}' and brand='{sql_data['brand']}'")

            response = result.fetchall()

            if not response:
                self.cursor.execute("INSERT OR IGNORE INTO statistic ('marketplace', 'brand',"
                                    "'orders', 'profit', 'date') VALUES (?,?,?,?,?)",
                                    (sql_data['marketplace'], sql_data['brand'],
                                     sql_data['orders'], sql_data['profit'], sql_data['date']))

                self.conn.commit()

                return True

            return True

        except Exception as es:
            import asyncio

            asyncio.run(logger_msg(f'Ошибка сохранения в базу данных "{es}"'))

            return False

    def close(self):
        self.conn.close()
        print('Отключился от SQL BD')
