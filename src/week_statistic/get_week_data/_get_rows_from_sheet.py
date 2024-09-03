# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from settings import MAX_ROWS
from src.google.google_core import LoopCreateGoogleCore
from src.logger._logger import logger_msg
from src.week_statistic.get_week_data._get_idx_columns import GetIdxColumnsWeek


async def get_rows_from_sheet(data_sheet):
    range_ = f'A1:XX{MAX_ROWS}'

    name_sheet = data_sheet['week_profit_tab']

    id_sheet = data_sheet['sheets']

    brand = data_sheet['brand']

    market_place = data_sheet['market_place']

    google_core = LoopCreateGoogleCore.create_core_google(id_sheet)

    if not google_core:
        error_ = f'Не cмог подключиться к таблице "{brand}" "{market_place}" "{id_sheet}"'

        await logger_msg(error_, push=True)

        return False

    data_week = google_core.loop_get_row_range(name_sheet, range_)

    if not data_week:
        return False

    data_week = [row for row in data_week if type(row) == list]

    idx_title = await GetIdxColumnsWeek(data_week[0]).get_idx_week()

    if not idx_title:
        return False

    await google_core.close_connect()

    return_dict = {
        'data_week': data_week,
        'idx_title': idx_title,
    }

    return return_dict
