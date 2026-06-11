# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from settings import MARKETPLACE, ACCESS, BRANDS_SEPARATE_STATS, BRANDS_ORDER
from src.get_message.filter_brand.filter_brand import filter_brand
from src.get_message.formate_row import formate_row


class SalesBlock:

    def __init__(self, settings):
        self.BotDB = settings['BotDB']

        self.target_day = settings['target_day']

        self.analyst_day = settings['analyst_day']

        self.user_id = settings['user_id']

        self.security_brand = ACCESS[str(self.user_id)]

        self.msg = '<b>Заказы по брендам:</b>\n'

    def _get_separate_brands_for_brand(self, brand):
        """
        Найти separate-бренды из BRANDS_SEPARATE_STATS которые:
        1) относятся к API-бренду (ключ contains в brand)
        2) ЕСТЬ В ДОСТУПЕ у пользователя (self.security_brand)
        
        Args:
            brand: API-бренд (например "Kronly")
            
        Returns:
            Список найденных брендов для отдельной статистики
        """
        if not BRANDS_SEPARATE_STATS:
            return []
        
        found_brands = []
        brand_lower = brand.lower()
        
        # Проверяем каждый separate-бренд
        for separate_lower, separate_name in BRANDS_SEPARATE_STATS.items():
            # Ключ (separate_lower) должен содержаться в brand
            if separate_lower in brand_lower:
                # И имя бренда должно быть в доступе пользователя
                if separate_name in self.security_brand:
                    found_brands.append(separate_name)
        
        return found_brands

    async def iter_market_place(self, brand):
        for marketplace in MARKETPLACE:

            stop_filter = filter_brand(marketplace, brand)

            if stop_filter:
                continue

            # Получаем статистику по основному бренду
            orders_now = self.BotDB.get_all_orders_by_brand_case(marketplace, brand, self.target_day, 'order')
            orders_yesterday = self.BotDB.get_all_orders_by_brand_case(marketplace, brand, self.analyst_day, 'order')

            orders_now_count = orders_now[0] if orders_now else 0
            orders_now_money = orders_now[1] if orders_now else 0
            orders_yesterday_count = orders_yesterday[0] if orders_yesterday else 0
            orders_yesterday_money = orders_yesterday[1] if orders_yesterday else 0

            data_row_text = await formate_row(
                (orders_now_count, orders_now_money),
                (orders_yesterday_count, orders_yesterday_money)
            )

            maximal_orders = self.BotDB.get_maximum_all_orders_by_brand(marketplace, brand, 'order')

            if maximal_orders and orders_now:
                maximal_orders_one = maximal_orders[0] if maximal_orders[0] else 0
                maximal_orders_second = maximal_orders[1] if maximal_orders[1] else 0

                if (orders_now_count >= maximal_orders_one and maximal_orders_one) or (
                        orders_now_money >= maximal_orders_second and maximal_orders_second):
                    data_row_text = f"{data_row_text} 🍾🟢"

            self.msg += f'{brand} ({marketplace.upper()}): {data_row_text}\n'

        return True

    async def iter_brands(self):
        # Собираем все бренды (основные + separate)
        all_brands = list(self.security_brand)
        
        # Сортируем бренды по BRANDS_ORDER (если есть), иначе по алфавиту
        def get_brand_priority(brand):
            if BRANDS_ORDER and brand in BRANDS_ORDER:
                return BRANDS_ORDER[brand]
            # Большое число чтобы бренды без порядка были в конце
            return 999
        
        sorted_brands = sorted(all_brands, key=get_brand_priority)
        
        for i, brand in enumerate(sorted_brands):
            result = await self.iter_market_place(brand)

            if i < len(sorted_brands) - 1:
                next_brand = sorted_brands[i + 1]
                if next_brand != 'Kronly Agent':
                    self.msg += '\n'

        return True

    async def start_sales_block(self):
        result = await self.iter_brands()

        return self.msg
