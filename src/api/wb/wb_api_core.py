# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
import aiohttp


class WBApiCore:
    def __init__(self):
        self.url_statistic = f'https://statistics-api.wildberries.ru/'

        self.url_content = f'https://suppliers-api.wildberries.ru/'

        self.url_advert = f'https://advert-api.wb.ru/adv/'

        self.url_discount = f'https://discounts-prices-api.wildberries.ru/'

        self.new_analitic_url = f'https://seller-analytics-api.wildberries.ru/'

        self.time_try = 15

        self.count_try = 10

        self.session_timeout = aiohttp.ClientTimeout(total=1, connect=.1)
