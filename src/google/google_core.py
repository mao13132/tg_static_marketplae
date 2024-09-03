import os
import time
from datetime import datetime

from oauth2client.service_account import ServiceAccountCredentials

import gspread

from settings import API_KEY_GOOGLE, program_dir
from src.logger.logger_no_sync import logger_no_sync
from src.logger.telegram.telegram_debug_no_sync import SendlerOneCreate


class LoopCreateGoogleCore:
    @staticmethod
    def create_core_google(ID_SHEET):
        for _try in range(15):

            try:
                connect = ConnectGoogleCore(ID_SHEET)
            except Exception as es:
                logger_no_sync(f'Ошибка подключение к google sheet "{es}"')

                time.sleep(300)

                continue

            if not connect.sheet:
                logger_no_sync(f'Нет соединения с таблицей "{ID_SHEET}" - пробую ещё')

                time.sleep(300)

                continue

            return connect

        msg = f'DDR GoogleCore: ' \
              f'Не смог создать подключение к google таблице ' \
              f'"{ID_SHEET}" все попытки создать google подключение исчерпаны'

        logger_no_sync(msg)

        SendlerOneCreate('').save_text(msg)

        return False


class ConnectGoogleCore:
    def __init__(self, ID_SHEET):
        try:

            self.count_try = 5

            self.sleep_try = 10

            self.micro_sleep = 1

            json_keyfile = f'{program_dir}{os.sep}src{os.sep}google{os.sep}keys{os.sep}{API_KEY_GOOGLE}'

            scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

            credentials = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile, scope)

            self.gc = gspread.authorize(credentials)

            self.sheet = self.gc.open_by_key(ID_SHEET)

        except Exception as es:
            logger_no_sync(f'Ошибка при создания подключения google_core "{es}"')

            self.sheet = False

    def _get_percent_format(self, name_sheet, request_data):
        try:
            worksheet = self.sheet.worksheet(name_sheet)

            requests = []

            for range_ in request_data:
                requests.append(
                    {
                        "repeatCell": {
                            "range": {
                                "sheetId": worksheet.id,
                                "startRowIndex": range_["row"] - 1,
                                "endRowIndex": range_["row"],
                                "startColumnIndex": range_["drr_column"] - 1,
                                "endColumnIndex": range_["drr_column"]
                            },

                            'cell': {
                                'userEnteredFormat': {
                                    'numberFormat': {
                                        'type': 'PERCENT',
                                        # 'pattern': '.0%'
                                        'pattern': '0.00%'
                                    },
                                },
                            },
                            "fields": "userEnteredFormat.numberFormat"

                        }
                    }
                )

            body = {
                'requests': requests
            }

            self.sheet.batch_update(body)

        except Exception as es:
            logger_no_sync(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
                               f'Ошибка _get_percent_format имя вкладки "{name_sheet}": "{es}"')

            return False

        return True

    def _create_group(self, name_sheet, start_idx, end_idx):
        try:
            worksheet = self.sheet.worksheet(name_sheet)

            requests = [{
                "addDimensionGroup": {
                    "range": {
                        "sheetId": worksheet.id,
                        "dimension": "ROWS",
                        "startIndex": start_idx,
                        "endIndex": end_idx
                    }
                }
            }]

            body = {
                'requests': requests
            }

            self.sheet.batch_update(body)

        except Exception as es:
            logger_no_sync(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
                               f'Ошибка _create_group имя вкладки "{name_sheet}": "{es}"')

            return False

        return True

    def loop_create_group(self, name_sheet, start_idx, end_idx):

        for _try in range(self.count_try):

            res_update = self._create_group(name_sheet, start_idx, end_idx)

            if not res_update:
                time.sleep(self.sleep_try)

                continue

            return True

        msg = f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} ' \
              f'GoogleCore: Исчерпал все попытки google_core loop_create_group "{name_sheet}"'

        logger_no_sync(msg)

        SendlerOneCreate('').save_text(msg)

        return False

    def _close_group(self, name_sheet, start_idx, end_idx):
        try:
            worksheet = self.sheet.worksheet(name_sheet)

            requests = [
                {
                    "updateDimensionGroup": {
                        "dimensionGroup": {
                            "range": {
                                "sheetId": worksheet.id,
                                "dimension": "ROWS",
                                "startIndex": start_idx,
                                "endIndex": end_idx
                            },

                            "collapsed": True,
                            "depth": 1
                        },

                        "fields": "collapsed"
                    }
                }
            ]
            body = {
                'requests': requests
            }
            self.sheet.batch_update(body)

        except Exception as es:
            # logger_msg_no_sync(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
            #            f'Ошибка _close_group имя вкладки "{name_sheet}": "{es}"')

            return False

        return True

    def loop_close_group(self, name_sheet, start_idx, end_idx):

        for _try in range(1):

            res_update = self._close_group(name_sheet, start_idx, end_idx)

            if not res_update:
                time.sleep(self.sleep_try)

                continue

            return True

        msg = f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} ' \
              f'GoogleCore: Исчерпал все попытки google_core loop_close_group "{name_sheet}"'

        logger_no_sync(msg)

        # SendlerOneCreate('').save_text(msg)

        return False

    def _delete_group(self, name_sheet, start_idx, end_idx):
        try:
            worksheet = self.sheet.worksheet(name_sheet)

            requests = [{
                "deleteDimensionGroup": {
                    "range": {
                        "sheetId": worksheet.id,
                        "dimension": "ROWS",
                        "startIndex": start_idx,
                        "endIndex": end_idx
                    }
                }
            }]

            body = {
                'requests': requests
            }

            self.sheet.batch_update(body)

        except Exception as es:
            logger_no_sync(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
                               f'Ошибка _create_group имя вкладки "{name_sheet}": "{es}"')

            return False

        return True

    def loop_delete_group(self, name_sheet, start_idx, end_idx):

        for _try in range(1):

            res_update = self._delete_group(name_sheet, start_idx, end_idx)

            if not res_update:
                time.sleep(self.sleep_try)

                continue

            return True

        # msg = f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} ' \
        #       f'GoogleCore: Исчерпал все попытки google_core loop_delete_group "{name_sheet}"'

        # logger_msg_no_sync(msg)

        # SendlerOneCreate('').save_text(msg)

        return False

    def _merge_range(self, name_sheet, ranges_merge):

        try:
            worksheet = self.sheet.worksheet(name_sheet)

            requests = []

            for range_ in ranges_merge:
                requests.append(
                    {
                        "mergeCells": {
                            "range": {
                                "sheetId": worksheet.id,
                                "startRowIndex": range_["startRowIndex"],
                                "endRowIndex": range_["endRowIndex"],
                                "startColumnIndex": range_["startColumnIndex"],
                                "endColumnIndex": range_["endColumnIndex"]
                            },
                            "mergeType": "MERGE_ALL"
                        }
                    }
                )

            body = {
                'requests': requests
            }

            self.sheet.batch_update(body)

        except Exception as es:
            logger_no_sync(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
                               f'GoogleCore:  _merge_range "{es}"')

            return False

        return True

    def loop_merge_range(self, name_sheet, ranges_merge):

        for _try in range(self.count_try):

            res_update = self._merge_range(name_sheet, ranges_merge)

            if not res_update:
                time.sleep(self.sleep_try)

                continue

            return True

        msg = f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} ' \
              f'GoogleCore: Исчерпал все попытки google_core loop_merge_range "{name_sheet}"'

        logger_no_sync(msg)

        SendlerOneCreate('').save_text(msg)

        return False

    def _get_worksheet(self, name_sheet):

        try:

            worksheet = self.sheet.worksheet(name_sheet)

        except Exception as es:
            logger_no_sync(f'Не смог получить worksheet _get_worksheet: "{name_sheet}" "{es}"')

            return False

        return worksheet

    def loop_get_worksheet(self, name_sheet):
        for _try in range(self.count_try):
            worksheet = self._get_worksheet(name_sheet)

            if not worksheet:
                time.sleep(self.sleep_try)

                continue

            return worksheet

        msg = f'Все попытки получить worksheet у {name_sheet} закончились'

        logger_no_sync(msg)

        SendlerOneCreate('').save_text(msg)

        return False

    def _get_name_sheets(self):

        try:

            list_title_sheet = self.sheet.worksheets()

            list_name = [x.title for x in list_title_sheet]

        except Exception as es:
            logger_no_sync(f'Не смог получить имя вкладок "{es}"')

            return False

        return list_name

    def loop_get_name_sheets(self):
        for _try in range(self.count_try):
            list_title_sheet = self._get_name_sheets()

            if not list_title_sheet:
                time.sleep(self.sleep_try)

                continue

            return list_title_sheet

        msg = f'Все попытки получить ммя вкладок исчерпаны'

        logger_no_sync(msg)

        SendlerOneCreate('').save_text(msg)

        return False

    def _insert_rows(self, name_sheet, start_idx, end_idx):
        try:
            worksheet = self.sheet.worksheet(name_sheet)

            requests = [{
                "insertDimension": {
                    "range": {
                        "sheetId": worksheet.id,
                        "dimension": "ROWS",
                        "startIndex": start_idx,
                        "endIndex": end_idx
                    },
                    "inheritFromBefore": True
                }
            }]

            body = {
                'requests': requests
            }

            self.sheet.batch_update(body)

        except Exception as es:
            logger_no_sync(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
                               f'Ошибка _insert_rows имя вкладки "{name_sheet}": "{es}"')

            return False

        return True

    def loop_insert_rows(self, name_sheet, start_idx, end_idx):
        for _try in range(self.count_try):

            range_date_list = self._insert_rows(name_sheet, start_idx, end_idx)

            if not range_date_list:
                time.sleep(self.sleep_try)

                continue

            return range_date_list

        msg = f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} ' \
              f'GoogleCore: Все попытки вставить строчку на вкладку "{name_sheet}" исчерпаны'

        logger_no_sync(msg)

        SendlerOneCreate('').save_text(msg)

        return False

    def _insert_border_cell(self, name_sheet, start_idx_col, end_idx_col, start_row, end_row):
        try:
            worksheet = self.sheet.worksheet(name_sheet)

            requests = [{"updateBorders": {
                "range": {
                    "sheetId": worksheet.id,
                    "startRowIndex": start_row,
                    "endRowIndex": end_row,
                    "startColumnIndex": start_idx_col,
                    "endColumnIndex": end_idx_col
                },
                "top": {
                    "style": "SOLID",
                    "width": 1,
                },
                "bottom": {
                    "style": "SOLID",
                    "width": 1,
                },
                "innerHorizontal": {
                    "style": "SOLID",
                    "width": 1,
                },
                "innerVertical": {
                    "style": "SOLID",
                    "width": 1,
                },
            }
            }]

            body = {
                'requests': requests
            }

            self.sheet.batch_update(body)

        except Exception as es:
            logger_no_sync(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
                               f'Ошибка _insert_border_cell имя вкладки "{name_sheet}": "{es}"')

            return False

        return True

    def loop_insert_border_columns(self, name_sheet, start_idx_col, end_idx_col, start_row, end_row):
        for _try in range(self.count_try):

            range_date_list = self._insert_border_cell(name_sheet, start_idx_col, end_idx_col, start_row, end_row)

            if not range_date_list:
                time.sleep(self.sleep_try)

                continue

            return range_date_list

        msg = f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} ' \
              f'GoogleCore: Все попытки вставить колонки на вкладку "{name_sheet}" исчерпаны'

        logger_no_sync(msg)

        SendlerOneCreate('').save_text(msg)

        return False

    def _insert_columns(self, name_sheet, start_idx, end_idx):
        try:
            worksheet = self.sheet.worksheet(name_sheet)

            requests = [{
                "insertDimension": {
                    "range": {
                        "sheetId": worksheet.id,
                        "dimension": "COLUMNS",
                        "startIndex": start_idx,
                        "endIndex": end_idx
                    },
                    "inheritFromBefore": True
                }
            }]

            body = {
                'requests': requests
            }

            self.sheet.batch_update(body)

        except Exception as es:
            logger_no_sync(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
                               f'Ошибка _insert_columns имя вкладки "{name_sheet}": "{es}"')

            return False

        return True

    def loop_insert_columns(self, name_sheet, start_idx, end_idx):
        for _try in range(self.count_try):

            range_date_list = self._insert_columns(name_sheet, start_idx, end_idx)

            if not range_date_list:
                time.sleep(self.sleep_try)

                continue

            return range_date_list

        msg = f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} ' \
              f'GoogleCore: Все попытки вставить колонки на вкладку "{name_sheet}" исчерпаны'

        logger_no_sync(msg)

        SendlerOneCreate('').save_text(msg)

        return False

    def _get_range_date_columns(self, name_sheet, _range):

        try:

            worksheet = self.sheet.worksheet(name_sheet)

            list_columns = worksheet.range(_range)

        except Exception as es:
            logger_no_sync(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
                               f'Ошибка _get_range_date_columns имя вкладки "{name_sheet}": "{es}"')

            return False

        return list_columns

    def _get_row_range(self, name_sheet, _range):

        try:

            worksheet = self.sheet.worksheet(name_sheet)

            list_columns = worksheet.get(_range)

        except Exception as es:
            logger_no_sync(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
                               f'Ошибка _get_range_date_columns имя вкладки "{name_sheet}": "{es}"')

            return False

        return list_columns

    def loop_get_range(self, name_sheet, _range):
        for _try in range(self.count_try):

            range_date_list = self._get_range_date_columns(name_sheet, _range)

            if not range_date_list:
                time.sleep(self.sleep_try)

                continue

            return range_date_list

        msg = f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} ' \
              f'GoogleCore: Все попытки получить данные с вкладки "{name_sheet}" исчерпаны'

        logger_no_sync(msg)

        SendlerOneCreate('').save_text(msg)

        return False

    def loop_get_row_range(self, name_sheet, _range):
        for _try in range(self.count_try):

            range_date_list = self._get_row_range(name_sheet, _range)

            if not range_date_list:
                time.sleep(self.sleep_try)

                continue

            return range_date_list

        msg = f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} ' \
              f'GoogleCore: Все попытки получить данные с вкладки "{name_sheet}" исчерпаны'

        logger_no_sync(msg)

        SendlerOneCreate('').save_text(msg)

        return False

    def write_in_cell(self, name_sheet, row, columns, data_):

        for _try in range(self.count_try):

            res_write = self._new_write_in_cell(name_sheet, row, columns, data_)

            if not res_write:
                time.sleep(self.sleep_try)

                continue

            return True

        msg = f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} ' \
              f'GoogleCore: Исчерпал все попытки google_core write_in_cell: "{name_sheet}"'

        logger_no_sync(msg)

        SendlerOneCreate('').save_text(msg)

        return False

    def _new_write_in_cell(self, name_sheet, row, columns, data_):

        try:

            worksheet = self.sheet.worksheet(name_sheet)

            worksheet.update_cell(row, columns, data_)

        except Exception as es:
            logger_no_sync(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
                               f'GoogleCore:  ошибки new_write_in_cell "{es}"')

            return False

        return True

    def loop_write_data_from_range(self, name_sheet, _range, data_):

        for _try in range(self.count_try):

            res_update = self._write_data_from_range(name_sheet, _range, data_)

            if not res_update:
                time.sleep(self.sleep_try)

                continue

            return True

        msg = f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} ' \
              f'GoogleCore: Исчерпал все попытки google_core write_in_range_account "{name_sheet}"'

        logger_no_sync(msg)

        SendlerOneCreate('').save_text(msg)

        return False

    def _write_data_from_range(self, name_sheet, _range, data_):

        try:

            worksheet = self.sheet.worksheet(name_sheet)

            worksheet.update(_range, [data_], value_input_option='USER_ENTERED')

        except Exception as es:
            logger_no_sync(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
                               f'GoogleCore:  _write_data_from_range "{es}"')

            return False

        return True

    def _clear_range(self, name_sheet, _range):

        try:

            worksheet = self.sheet.worksheet(name_sheet)

            worksheet.batch_clear([_range])

        except Exception as es:
            logger_no_sync(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
                               f'GoogleCore:  Ошибка очистки диапазона у "{name_sheet}" _clear_range "{es}"')

            return False

        return True

    def loop_clear_range(self, name_sheet, _range):

        for _try in range(self.count_try):

            res_clear = self._clear_range(name_sheet, _range)

            if not res_clear:
                time.sleep(self.sleep_try)

                continue

            return True

        msg = f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} ' \
              f'GoogleCore:  Исчерпал все попытки очистить рандж "{_range}" loop_clear_range ' \
              f'"{name_sheet}"'

        logger_no_sync(msg)

        SendlerOneCreate('').save_text(msg)

        return False

    def get_data_by_range(self, name_sheet, range_):
        for _try in range(self.count_try):
            try:
                worksheet = self.sheet.worksheet(name_sheet)
            except Exception as es:

                logger_no_sync(f'Ошибка get_data_by_range у вкладки "{name_sheet}" "{es}"')

                time.sleep(self.sleep_try)

                continue

            try:
                data = worksheet.get_values(range_)

                return data
            except Exception as es:

                logger_no_sync(f'Ошибка get_data_by_range у вкладки "{name_sheet}" "{es}"')

                time.sleep(self.sleep_try)

                continue

        msg = f' Booster Seo: все попытки get_data_by_range у вкладки "{name_sheet}" кончились'

        logger_no_sync(msg)

        SendlerOneCreate('').save_text(msg)

        return False

    def _new_write_data_from_range(self, name_sheet, _range, data_):

        try:

            worksheet = self.sheet.worksheet(name_sheet)

            worksheet.update(_range, data_)

        except Exception as es:
            logger_no_sync(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
                               f'GoogleCore:  _new_write_data_from_range "{es}"')

            return False

        return True

    def new_loop_write_data_from_range(self, name_sheet, _range, data_):

        for _try in range(self.count_try):

            res_update = self._new_write_data_from_range(name_sheet, _range, data_)

            if not res_update:
                time.sleep(self.sleep_try)

                continue

            return True

        msg = f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} ' \
              f'GoogleCore: Исчерпал все попытки google_core _new_write_in_range_account "{name_sheet}"'

        logger_no_sync(msg)

        SendlerOneCreate('').save_text(msg)

        return False

    async def close_connect(self):
        try:
            self.gc.session.close()
        except Exception as es:
            logger_no_sync(f'Не могу разорвать соединение "{es}"')

            return False

        return True
