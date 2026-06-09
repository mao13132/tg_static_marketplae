# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from settings import OZON_API_KEY_LIST, BRANDS_SEPARATE_STATS
from src.api.ozon.ozon_api_orders_profit import OzonApiOrdersProfit
from src.get_message.filter_brand.filter_brand import filter_brand
from src.get_data.ozon.process_separate_brand_stats import process_separate_brand_stats
from src.logger._logger import logger_msg


async def get_statistic_orders_ozon(BotDB, target_day):
    print(f'\nНачинаю получать данные о заказах с OZON\n')

    ozon_core = OzonApiOrdersProfit()

    is_good = True

    for brand, security in OZON_API_KEY_LIST.items():

        access_false = filter_brand('ozon', brand)

        if access_false:
            continue

        print(f'Начал обработку OZON: "{brand}"')

        # Получаем полные данные с товарами (rows)
        full_data = await ozon_core.loop_get_orders_profit_full(
            'TG BOT', security, target_day, target_day
        )

        if not full_data or full_data == '-1':
            await logger_msg(f'get_data_core: Не удалось получить данные ozon для "{brand}"')
            continue

        try:
            orders = full_data.get('orders', 0)
            profit = full_data.get('profit', 0)
            rows = full_data.get('rows', [])
        except Exception as es:
            await logger_msg(f'get_data_core: Не могу распарсить ответ ozon с заказами и профитом "{es}"')
            continue

        # Обработка брендов для отдельной статистики
        if BRANDS_SEPARATE_STATS and rows:
            result = await process_separate_brand_stats(
                security, brand, rows, BRANDS_SEPARATE_STATS, target_day
            )

            if result:
                # Сохраняем статистику по найденным брендам (исключение из общей)
                separate_stats = result.get('separate_stats', {})
                for found_brand, stats in separate_stats.items():
                    sql_data = {
                        'marketplace': 'ozon',
                        'brand': found_brand,  # Найденный бренд товара
                        'type': 'order',
                        'count': stats['orders'],
                        'money': stats['profit'],
                        'date': target_day,
                    }
                    BotDB.check_or_add_static(sql_data)
                    print(f'  -> Отдельная статистика: бренд "{found_brand}", '
                          f'{stats["orders"]} заказов, {stats["profit"]:.2f} выручки')

                # Вычитаем из основной статистики то, что ушло в отдельные бренды
                total_separate = result.get('total_separate', {})
                orders -= total_separate.get('orders', 0)
                profit -= total_separate.get('profit', 0)

        # Записываем основную статистику по API-ключу (за вычетом найденных брендов)
        if orders > 0 or profit > 0:
            sql_data = {
                'marketplace': 'ozon',
                'brand': brand,
                'type': 'order',
                'count': orders,
                'money': profit,
                'date': target_day,
            }

            res = BotDB.check_or_add_static(sql_data)

            if not res:
                is_good = False

        print(f'Обработал Ozon "{brand}"')

    print(f'Обработал все бренды по Ozon')

    return is_good
