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


class OzonApiSales(OzonApiCore):
    async def _get_sales(self, client_id, api_key, start_date):
        url_get_img = self.url_seller + f'v3/finance/transaction/list'

        header_ = {'Content-Type': 'application/json',
                   'Client-Id': client_id,
                   'Api-Key': api_key
                   }

        data_ = {
            "filter": {
                "date": {
                    "from": f"{start_date}T00:00:00.000Z",
                    "to": f"{start_date}T00:00:00.000Z"
                },
                "operation_type": ["OperationAgentDeliveredToCustomerCanceled"],
                "transaction_type": "orders"
            },
            "page": 1,
            "page_size": 1000
        }

        try:

            async with aiohttp.ClientSession(timeout=self.session_timeout) as session:
                async with session.post(url_get_img,
                                        timeout=aiohttp.ClientTimeout(total=60),
                                        headers=header_,
                                        json=data_) as resul:
                    response = await resul.json()

                    if resul.status == 200 and not response:
                        await logger_msg(f'OZON API SALES: Нулевой ответ от серверов')

                    return response

        except Exception as es:
            await logger_msg(f'OZON API SALES: Ошибка при получение данных о продажах "{es}"')

            return '-1'

    async def check_error(self, data_response, name_sheet):
        try:
            error = data_response['message']
        except:
            return False

        if 'too many requests' in error or 'rate limit' in error:
            print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
                  f'OZON API SALES check_error: Частые запросы - жду 60с у "{name_sheet}"')
            return '-1'

        msg = f'OZON API SALES: Ошибка при получения данных о продажах по API у {name_sheet}\n"{error}"'

        await logger_msg(msg, push=True)

        return True

    async def loop_get_sales_ozon(self, name_sheet, security, start_date):

        client_id, api_key = await get_api_key(security)

        if not client_id:
            return False

        for _try in range(self.count_try):
            data_response = await self._get_sales(client_id, api_key, start_date)

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
                result = data_response['result']['operations']
            except:
                continue

            return result

        msg = f'OZON API SALES: исчерпаны все попытки на получение данных о продажах у {name_sheet}'

        await logger_msg(msg, push=True)

        return False
