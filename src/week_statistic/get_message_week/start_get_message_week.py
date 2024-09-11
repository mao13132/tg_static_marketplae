# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from settings import ACCESS, SOURCE_SHEETS
from src.logger.logger_no_sync import logger_no_sync
from src.logger.telegram.telegram_debug_no_sync import SendlerOneCreate
from src.utils.clear_float import clear_float
from src.utils.generate_date import minus_days_week


class StartGetMessageWeek:
    def __init__(self, settings):
        self.settings = settings

        self.BotDB = settings['BotDB']

        self.user_id = settings['user_id']

        self.data = {}

    async def start_get_message_week(self):
        """Получаю данные за числовой диапазон из первой строчки, далее по этой дате ищу старые на 1 день данные,
        суммирую данные по маркетплейсам и возвращаю суммированные данные по брендам"""

        print(f'\nНачинаю формировать сообщение с недельными данными\n')

        pk_id_sql = []

        access_brand_list = [x for x in ACCESS[str(self.user_id)]]

        start_date_week = False

        end_date_week = False

        for brand in SOURCE_SHEETS:
            current_brand = brand['brand']

            marketplace = brand['market_place']

            if current_brand not in access_brand_list:
                continue

            week_data_row_list = self.BotDB.get_week_data(current_brand, marketplace, start_date_week, end_date_week)

            if not week_data_row_list:
                continue

            for week_data_row in week_data_row_list:

                pk_id_sql.append(week_data_row[0])

                # Устанавливаю дату, что бы собрать только за этот период
                start_date_week = week_data_row[4]

                end_date_week = week_data_row[5]

                date_minus_day = minus_days_week(start_date_week)

                old_week_data_row = self.BotDB.get_week_old_data(current_brand, marketplace, date_minus_day)

                if not old_week_data_row:
                    error_ = f'Нет старых данных для "{marketplace}" "{current_brand}" за "{date_minus_day}"'

                    logger_no_sync(error_)

                    SendlerOneCreate('').save_text(error_)

                    continue

                exists = self.data.get(current_brand, False)

                if not exists:
                    self.data[current_brand] = {
                        'sellers': 0,
                        'money': 0,
                        'old_sellers': 0,
                        'old_money': 0,
                        'start_date': start_date_week,
                        'end_date': end_date_week,
                    }

                self.data[current_brand]['sellers'] += week_data_row[6]

                self.data[current_brand]['money'] += await clear_float(week_data_row[7])

                self.data[current_brand]['old_sellers'] += old_week_data_row[6]

                self.data[current_brand]['old_money'] += await clear_float(old_week_data_row[7])

                continue

        if pk_id_sql:
            self.data['ids'] = pk_id_sql

        return self.data


if __name__ == '__main__':
    import asyncio

    from src.sql.bot_connector import BotDB

    settings_get_msg_week = {
        'BotDB': BotDB,
        'user_id': 1422194909,
    }

    res_ = asyncio.run(StartGetMessageWeek(settings_get_msg_week).start_get_message_week())
