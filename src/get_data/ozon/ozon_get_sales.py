# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from settings import OZON_API_KEY_LIST, BRANDS_SEPARATE_STATS
from src.api.ozon.ozon_api_sales import OzonApiSales
from src.get_message.filter_brand.filter_brand import filter_brand
from src.get_data.ozon.process_separate_brand_stats_for_sales import process_separate_brand_stats_for_sales
from src.logger._logger import logger_msg


async def get_statistic_sales_ozon(BotDB, target_day):
    print(f'\nНачинаю получать данные о продажах с OZON\n')

    ozon_core = OzonApiSales()

    is_good = True

    for brand, security in OZON_API_KEY_LIST.items():

        access_false = filter_brand('ozon', brand)

        if access_false:
            continue

        data_statistic = await ozon_core.loop_get_sales_ozon(
            brand, security, target_day)

        if not data_statistic:
            await logger_msg(f'get_data_core: Не удалось получить данные ozon продаж для "{brand}"')
            continue

        operations = data_statistic

        sales = len(operations)
        money = 0

        for sale in operations:
            money += sale['accruals_for_sale']

        # Обработка брендов для отдельной статистики
        if BRANDS_SEPARATE_STATS and operations:
            result = await process_separate_brand_stats_for_sales(
                security, brand, operations, BRANDS_SEPARATE_STATS, target_day
            )

            if result:
                # Сохраняем статистику по найденным брендам (исключение из общей)
                separate_stats = result.get('separate_stats', {})
                for found_brand, stats in separate_stats.items():
                    sql_data = {
                        'marketplace': 'ozon',
                        'brand': found_brand,  # Найденный бренд товара
                        'type': 'sale',
                        'count': stats['operations'],
                        'money': stats['money'],
                        'date': target_day,
                    }
                    BotDB.check_or_add_static(sql_data)
                    print(f'  -> Отдельная статистика: бренд "{found_brand}", '
                          f'{stats["operations"]} продаж, {stats["money"]:.2f} выручки')

                # Вычитаем из основной статистики то, что ушло в отдельные бренды
                total_separate = result.get('total_separate', {})
                sales -= total_separate.get('operations', 0)
                money -= total_separate.get('money', 0)

        # Записываем основную статистику по API-ключу (за вычетом найденных брендов)
        if sales > 0 or money > 0:
            sql_data = {
                'marketplace': 'ozon',
                'brand': brand,
                'type': 'sale',
                'count': sales,
                'money': money,
                'date': target_day,
            }

            res = BotDB.check_or_add_static(sql_data)

            if not res:
                is_good = False

        print(f'Обработал Ozon "{brand}"')

    print(f'Обработал все бренды по Ozon')

    return is_good
