# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
import time
from datetime import datetime

import aiohttp

from src.api.ozon.get_api_key import get_api_key
from src.logger._logger import logger_msg
from src.api.ozon.ozon_api_core import OzonApiCore


class OzonApiOrdersProfit(OzonApiCore):
    async def _get_orders_profit(self, client_id, api_key, start_date, end_date):
        url_get_img = self.url_seller + f'v1/analytics/data'

        header_ = {'Content-Type': 'application/json',
                   'Client-Id': client_id,
                   'Api-Key': api_key
                   }

        data_ = {
            "date_from": start_date,
            "date_to": end_date,
            "metrics": [
                "ordered_units", "revenue"
            ],
            "dimension": [
                "sku",
                "day"
            ],
            "filters": [],
            "sort": [
                {
                    "key": "sku",
                    "order": "DESC"
                }
            ],
            "limit": 1000,
            "offset": 0
        }

        try:

            async with aiohttp.ClientSession(timeout=self.session_timeout) as session:
                async with session.post(url_get_img,
                                        timeout=aiohttp.ClientTimeout(total=60),
                                        headers=header_,
                                        json=data_) as resul:
                    response = await resul.json()

                    if resul.status == 200 and not response:
                        await logger_msg(f'OZON API ORDERS PROFIT: Нулевой ответ от серверов')

                    return response

        except Exception as es:
            await logger_msg(f'OZON API ORDERS PROFIT: Ошибка при получение order-profit "{es}"')

            return '-1'

    async def check_error(self, data_response, name_sheet):
        try:
            error = data_response['message']
        except:
            return False

        if 'too many requests' in error or 'rate limit' in error:
            print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
                  f'OZON API ORDERS PROFIT check_error: Частые запросы - жду 60с у "{name_sheet}"')
            return '-1'

        msg = f'OZON API ORDERS PROFIT: Ошибка при получения order-profit по API у {name_sheet}\n"{error}"'

        await logger_msg(msg, push=True)

        return True

    async def loop_get_orders_profit(self, name_sheet, security, start_date, end_date):

        client_id, api_key = await get_api_key(security)

        if not client_id:
            return False

        for _try in range(self.count_try):
            data_response = await self._get_orders_profit(client_id, api_key, start_date, end_date)

            if data_response == '-1':
                time.sleep(self.time_try)

                continue

            if not data_response:
                continue

            is_error = await self.check_error(data_response, name_sheet)

            if is_error == '-1':
                time.sleep(60)

                continue

            if is_error:
                continue

            try:
                result = data_response['result']['totals']
            except:
                continue

            return result

        msg = f'OZON API ORDERS PROFIT: исчерпаны все попытки на получение order-profit у {name_sheet}'

        await logger_msg(msg, push=True)

        return False

    async def _get_orders_profit_paged(self, client_id, api_key, start_date, end_date, offset):
        """Получить данные заказов с пагинацией"""
        url_get_img = self.url_seller + f'v1/analytics/data'

        header_ = {'Content-Type': 'application/json',
                   'Client-Id': client_id,
                   'Api-Key': api_key
                   }

        data_ = {
            "date_from": start_date,
            "date_to": end_date,
            "metrics": [
                "ordered_units", "revenue"
            ],
            "dimension": [
                "sku",
                "day"
            ],
            "filters": [],
            "sort": [
                {
                    "key": "sku",
                    "order": "DESC"
                }
            ],
            "limit": 1000,
            "offset": offset
        }

        try:

            async with aiohttp.ClientSession(timeout=self.session_timeout) as session:
                async with session.post(url_get_img,
                                        timeout=aiohttp.ClientTimeout(total=60),
                                        headers=header_,
                                        json=data_) as resul:
                    response = await resul.json()

                    return response

        except Exception as es:
            await logger_msg(f'OZON API ORDERS PROFIT: Ошибка при получение order-profit paged "{es}"')

            return '-1'

    async def loop_get_orders_profit_full(self, name_sheet, security, start_date, end_date):
        """Получить полные данные заказов с товарами (data)"""
        client_id, api_key = await get_api_key(security)

        if not client_id:
            return False

        all_rows = []
        total_orders = 0
        total_profit = 0
        offset = 0

        while True:
            for _try in range(self.count_try):
                data_response = await self._get_orders_profit_paged(
                    client_id, api_key, start_date, end_date, offset
                )

                if data_response == '-1':
                    time.sleep(self.time_try)
                    continue

                if not data_response:
                    continue

                is_error = await self.check_error(data_response, name_sheet)

                if is_error == '-1':
                    time.sleep(60)
                    continue

                if is_error:
                    continue

                try:
                    result = data_response['result']
                    totals = result.get('totals', [])
                    # API возвращает данные в 'data', а не в 'rows'
                    rows = result.get('data', [])

                    if totals and len(totals) >= 2:
                        total_orders += int(totals[0])
                        total_profit += float(totals[1])

                    all_rows.extend(rows)

                    # Проверяем есть ли ещё данные
                    if len(rows) < 1000:
                        # Это была последняя страница
                        return {
                            'orders': total_orders,
                            'profit': total_profit,
                            'rows': all_rows
                        }

                    offset += 1000

                except Exception as es:
                    await logger_msg(f'OZON API ORDERS PROFIT: Ошибка парсинга data "{es}"')
                    break

            # Если исчерпали попытки на одной странице, выходим
            break

        return {
            'orders': total_orders,
            'profit': total_profit,
            'rows': all_rows
        }
