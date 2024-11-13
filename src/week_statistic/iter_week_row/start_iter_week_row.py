# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from src.utils.clear_float import clear_int, clear_float


class StartIterWeekRow:
    def __init__(self, settings):
        self.settings = settings

        self.data_week = settings['data_week']

        self.idx_title = settings['idx_title']

        self.BotDB = settings['BotDB']

        self.data_sheet = settings['data_sheet']

    async def start_iter_week_row(self):
        for count_row, row in enumerate(self.data_week[1:]):
            if not row:
                continue

            idx_numbers = self.idx_title['idx_numbers']

            number_report = row[idx_numbers]

            if not number_report:
                continue

            marketplace = self.data_sheet['market_place']

            brand = self.data_sheet['brand']

            idx_start_date = self.idx_title['idx_start_date']

            start_date = row[idx_start_date]

            if len(start_date) == 9:
                start_date = f'0{start_date}'

            idx_end_date = self.idx_title['idx_end_date']

            end_date = row[idx_end_date]

            if len(end_date) == 9:
                end_date = f'0{end_date}'

            idx_sellers = self.idx_title['idx_sellers']

            sellers = row[idx_sellers]

            sellers = await clear_int(sellers)

            idx_total_profit = self.idx_title['idx_total_profit']

            profit = row[idx_total_profit]

            profit = await clear_float(profit)

            exists = self.BotDB.check_or_add_week(number_report, marketplace, brand, start_date,
                                                  end_date, sellers, profit)

            continue

        return True
