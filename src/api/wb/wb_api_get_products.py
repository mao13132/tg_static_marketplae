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

from src.api.wb.get_api_key import wb_get_api_key
from src.api.wb.wb_api_core import WBApiCore
from src.logger._logger import logger_msg


class WBApiGetProducts(WBApiCore):
    async def _get_products(self, api_key):
        url_get_img = self.url_discount + f'api/v2/list/goods/filter?limit=1000'

        headers_price = {'Content-Type': 'application/json',
                         'Authorization': api_key
                         }

        try:

            async with aiohttp.ClientSession(timeout=self.session_timeout) as session:
                async with session.get(url_get_img,
                                       timeout=aiohttp.ClientTimeout(total=60),
                                       headers=headers_price) as resul:
                    response = await resul.json()

                    if resul.status == 200 and not response:
                        await logger_msg(f'WB API Products: Нулевой ответ от серверов WB ')

                        return False

                    return response

        except Exception as es:
            await logger_msg(f'WB API Products: Ошибка при получение продуктов "{es}"')

            return '-1'

    async def check_error(self, data_response, brand):
        try:
            error = data_response['message']
        except:
            return False

        if 'too many requests' in error:
            print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
                  f'WB API Products check_error: Частые запросы - жду {self.time_try}с у "{brand}"')
            return '-1'

        msg = f'WB API Products: Ошибка при получение продуктов по API у {brand}\n"{error}"'

        await logger_msg(msg, push=True)

        return True

    async def loop_get_products(self, brand):

        api_key = await wb_get_api_key(brand, 1)

        if not api_key:
            return False

        for _try in range(self.count_try):
            data_response = await self._get_products(api_key)

            if data_response == '-1':
                time.sleep(self.time_try)

                continue

            if not data_response:
                return False

            is_error = await self.check_error(data_response, brand)

            if is_error == '-1':
                time.sleep(self.time_try)

                continue

            if is_error:
                return False

            try:
                result = data_response['data']['listGoods']
            except:
                continue

            return result

        msg = f'WB API Products: исчерпаны все попытки на получение продуктов у {brand}'

        await logger_msg(msg, push=True)

        return False
