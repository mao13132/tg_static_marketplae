# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from src.logger.logger_no_sync import logger_no_sync
from src.logger.telegram.telegram_debug_no_sync import SendlerOneCreate


class GetIdxColumnsWeek:
    def __init__(self, title_row):
        self.column_numbers = 'Номер отчета'

        self.column_start_date = 'Дата начала'

        self.column_end_date = 'Дата конца'

        self.column_sellers = 'Продажа (Кол-во = суммарное количество продаж)'

        self.column_profit = 'К перечислению за товар = К перечислению Продавцу за реализованный Товар'

        self.column_cost_shep = 'Стоимость логистики = Услуги по доставке товара покупателю'

        self.column_fine = 'Общая сумма штрафов =/='

        self.column_add_pay = 'Доплаты =/='

        self.column_storage = 'Стоимость хранения = Хранение'

        self.column_paid = 'Стоимость платной приемки = Платная приемка'

        self.column_deductions = 'Прочие удержания = Удержания'

        self.column_cash_back_ship = 'Возмещение издержек по перевозке/по складским операциям с товаром'

        self.column_summa_from_pay = 'Итого к оплате'

        self.column_ads = 'Реклама по апи'

        self.column_material_cost = 'Материальная себестоимость'

        self.column_total_profit = 'Прибыль'

        self.title_row = title_row

    def _get_idx_columns(self, title):
        try:
            idx = self.title_row.index(title)

        except Exception as es:
            error_ = f'Не могу найти колонку с "{title}" в строке "{self.title_row}" не могу записать week данные "{es}"'

            logger_no_sync(error_)

            SendlerOneCreate('').save_text(error_)

            return False

        return idx

    async def get_idx_week(self):

        idx_numbers = self._get_idx_columns(self.column_numbers)

        if str(idx_numbers) == 'False':
            return False

        idx_start_date = self._get_idx_columns(self.column_start_date)

        if str(idx_start_date) == 'False':
            return False

        idx_end_date = self._get_idx_columns(self.column_end_date)

        if str(idx_end_date) == 'False':
            return False

        idx_sellers = self._get_idx_columns(self.column_sellers)

        if str(idx_sellers) == 'False':
            return False

        idx_profit = self._get_idx_columns(self.column_profit)

        if str(idx_profit) == 'False':
            return False

        idx_shep = self._get_idx_columns(self.column_cost_shep)

        if str(idx_shep) == 'False':
            return False

        idx_fine = self._get_idx_columns(self.column_fine)

        if str(idx_fine) == 'False':
            return False

        idx_add_pay = self._get_idx_columns(self.column_add_pay)

        if str(idx_add_pay) == 'False':
            return False

        idx_storage = self._get_idx_columns(self.column_storage)

        if str(idx_storage) == 'False':
            return False

        idx_paid = self._get_idx_columns(self.column_paid)

        if str(idx_paid) == 'False':
            return False

        idx_deductions = self._get_idx_columns(self.column_deductions)

        if str(idx_deductions) == 'False':
            return False

        idx_cash_back_ship = self._get_idx_columns(self.column_cash_back_ship)

        if str(idx_cash_back_ship) == 'False':
            return False

        idx_summa_from_pay = self._get_idx_columns(self.column_summa_from_pay)

        if str(idx_summa_from_pay) == 'False':
            return False

        idx_column_ads = self._get_idx_columns(self.column_ads)

        if str(idx_column_ads) == 'False':
            return False

        idx_material_cost = self._get_idx_columns(self.column_material_cost)

        if str(idx_material_cost) == 'False':
            return False

        idx_total_profit = self._get_idx_columns(self.column_total_profit)

        if str(idx_total_profit) == 'False':
            return False

        return_dict = {
            'idx_numbers': idx_numbers,
            'idx_start_date': idx_start_date,
            'idx_end_date': idx_end_date,
            'idx_sellers': idx_sellers,
            'idx_profit': idx_profit,
            'idx_shep': idx_shep,
            'idx_fine': idx_fine,
            'idx_add_pay': idx_add_pay,
            'idx_storage': idx_storage,
            'idx_paid': idx_paid,
            'idx_deductions': idx_deductions,
            'idx_cash_back_ship': idx_cash_back_ship,
            'idx_summa_from_pay': idx_summa_from_pay,
            'idx_column_ads': idx_column_ads,
            'idx_material_cost': idx_material_cost,
            'idx_total_profit': idx_total_profit,
        }

        return return_dict
