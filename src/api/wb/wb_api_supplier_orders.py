# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2025    Supplier Orders client
#
# ---------------------------------------------
import time
from datetime import datetime

import aiohttp

from src.api.wb.get_api_key import wb_get_api_key
from src.api.wb.wb_api_core import WBApiCore
from src.logger._logger import logger_msg


class WBApiSupplierOrders(WBApiCore):
    async def _get_orders(self, api_key, date_from, flag=1):
        url = self.url_statistic + 'api/v1/supplier/orders'

        headers = {
            'Content-Type': 'application/json',
            'Authorization': api_key
        }

        params = {
            'dateFrom': date_from,
            'flag': flag
        }

        try:
            async with aiohttp.ClientSession(timeout=self.session_timeout) as session:
                async with session.get(
                    url,
                    timeout=aiohttp.ClientTimeout(total=60),
                    headers=headers,
                    params=params
                ) as res:
                    if res.status == 200:
                        return await res.json()

                    try:
                        error_body = await res.json()
                    except Exception:
                        error_body = {'detail': f'HTTP {res.status}'}

                    try:
                        msg = error_body.get('detail') or error_body.get('message') or str(error_body)
                    except Exception:
                        msg = f'HTTP {res.status}'

                    if res.status in (429, 503):
                        await logger_msg(
                            f'WB Supplier Orders: too many requests or service unavailable, will retry: "{msg}"'
                        )
                        return '-1'

                    await logger_msg(f'WB Supplier Orders: error response "{msg}"', push=True)
                    return False
        except Exception as es:
            await logger_msg(f'WB Supplier Orders: exception "{es}"')
            return '-1'

    async def loop_get_orders_for_date(self, brand, date_from):
        api_key = await wb_get_api_key(brand, 0)
        if not api_key:
            return False

        for _try in range(self.count_try):
            data_response = await self._get_orders(api_key, date_from, flag=1)

            if data_response == '-1':
                time.sleep(self.time_try)
                continue

            if data_response is False:
                return False

            if isinstance(data_response, list):
                return data_response

            try:
                if isinstance(data_response, dict) and 'data' in data_response:
                    return data_response['data']
            except Exception:
                pass

            time.sleep(self.time_try)
            continue

        await logger_msg(f'WB Supplier Orders: exhausted retries for "{brand}"', push=True)
        return False

