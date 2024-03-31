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
                                f"type TEXT, "
                                f"count NUMERIC, "
                                f"money FLOAT, "
                                f"date DATETIME, "
                                f"other TEXT)")

        except Exception as es:
            print(f'SQL исключение check_table statistic {es}')

        try:
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS "
                                f"settings (id_pk INTEGER PRIMARY KEY AUTOINCREMENT, "
                                f"key TEXT, "
                                f"value TEX)")

        except Exception as es:
            print(f'SQL исключение settings {es}')

    def edit_settings(self, key, value):

        result = self.cursor.execute(f"SELECT value FROM settings "
                                     f"WHERE key = '{key}'")

        response = result.fetchall()

        if not response:
            self.cursor.execute("INSERT OR IGNORE INTO settings ('key', 'value') VALUES (?,?)",
                                (key, value))

            self.conn.commit()

            return True

        else:
            self.cursor.execute(f"UPDATE settings SET value = '{value}' WHERE key = '{key}'")

            self.conn.commit()

            return True

    def get_settings_by_key(self, key):

        result = self.cursor.execute(f"SELECT value FROM settings "
                                     f"WHERE key = '{key}'")

        response = result.fetchall()

        try:
            result = response[0][0]
        except:
            return False

        return result

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

            result = self.cursor.execute(
                f"SELECT id_pk, count, money FROM statistic WHERE type='{sql_data['type']}' and "
                f"date='{sql_data['date']}' and marketplace='{sql_data['marketplace']}' "
                f"and brand='{sql_data['brand']}'")

            response = result.fetchall()

            if not response:
                self.cursor.execute("INSERT OR IGNORE INTO statistic ('marketplace', 'brand', 'type',"
                                    "'count', 'money', 'date') VALUES (?,?,?,?,?,?)",
                                    (sql_data['marketplace'], sql_data['brand'],
                                     sql_data['type'], sql_data['count'], sql_data['money'], sql_data['date']))

                self.conn.commit()

                return True

            id_pk, count, money = response[0]

            if count != sql_data['count'] or money != sql_data['money']:
                self.cursor.execute(f"UPDATE statistic SET count = '{sql_data['count']}', "
                                    f"money = '{sql_data['money']}'  WHERE id_pk = '{id_pk}'")

                self.conn.commit()

                return True

            return True

        except Exception as es:
            import asyncio

            asyncio.run(logger_msg(f'Ошибка сохранения в базу данных "{es}"'))

            return False

    def get_all_orders_by_marketplace(self, marketplace, day, _type):
        try:

            result = self.cursor.execute(f"SELECT SUM(count), SUM(money) FROM statistic "
                                         f"WHERE marketplace = '{marketplace}' AND "
                                         f"date = '{day}' AND type = '{_type}'")

            response = result.fetchall()

            response = response[0]


        except Exception as es:
            print(f'Ошибка SQL get_all_orders_by_marketplace: {es}')

            return 0, 0

        return response

    def get_all_orders_by_brand(self, marketplace, brand, day, _type):
        try:

            result = self.cursor.execute(f"SELECT count, money FROM statistic "
                                         f"WHERE marketplace = '{marketplace}' AND "
                                         f"brand = '{brand}' AND "
                                         f"date = '{day}' AND type = '{_type}'")

            response = result.fetchall()

            try:
                response = response[0]
            except:
                return 0, 0


        except Exception as es:
            print(f'Ошибка SQL get_all_orders_by_brand: {es}')

            return 0, 0

        return response

    def get_all_marketplace_by_brands(self, brand, day, _type):
        try:

            result = self.cursor.execute(f"SELECT SUM(count), SUM(money) FROM statistic "
                                         f"WHERE brand = '{brand}' AND "
                                         f"date = '{day}' AND type = '{_type}'")

            response = result.fetchall()

            response = response[0]


        except Exception as es:
            print(f'Ошибка SQL get_all_marketplace_by_brands: {es}')

            return 0, 0

        return response

    def close(self):
        self.conn.close()
        print('Отключился от SQL BD')
