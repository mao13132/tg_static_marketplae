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

# if __name__ == '__main__':
#     import asyncio
#
#     from src.utils.generate_date import minus_days
#
#     day = minus_days(1)
#
#     res = asyncio.run(OzonApiOrdersProfit().loop_get_orders_profit('TG BOT', 'security', day, day))
#
#     print()
