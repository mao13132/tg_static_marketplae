# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
import aiohttp


class OzonApiCore:
    def __init__(self):
        self.url_seller = f'https://api-seller.ozon.ru/'

        self.url_performance = f'https://performance.ozon.ru/'

        self.url_performance_port = f'https://performance.ozon.ru:443/'

        self.time_try = 15

        self.count_try = 10

        self.session_timeout = aiohttp.ClientTimeout(total=1, connect=.1)
