# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from settings import SOURCE_SHEETS
from src.week_statistic.get_week_data._get_rows_from_sheet import get_rows_from_sheet
from src.week_statistic.iter_week_row.start_iter_week_row import StartIterWeekRow


class StartGetWeekData:
    def __init__(self, settings):
        self.settings = settings

        self.BotDB = settings['BotDB']

    async def start_get_week(self):
        for data_sheet in SOURCE_SHEETS:

            data_week_by_brand = await get_rows_from_sheet(data_sheet)

            if not data_week_by_brand:
                continue

            settings_write = {
                'data_week': data_week_by_brand['data_week'],
                'idx_title': data_week_by_brand['idx_title'],
                'BotDB': self.BotDB,
                'data_sheet': data_sheet,
            }

            res_write = await StartIterWeekRow(settings_write).start_iter_week_row()

            continue

        print(f'GetWeekData: Обработал все таблицы')

        return True


if __name__ == '__main__':
    import asyncio

    from src.sql.bot_connector import BotDB

    res_ = asyncio.run(StartGetWeekData({'BotDB': BotDB}).start_get_week())
