# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from settings import WB_API_KEY_LIST, BRANDS_SEPARATE_STATS
from src.api.wb.wb_api_sales import WBApiSales
from src.get_message.filter_brand.filter_brand import filter_brand
from src.get_data.wb.process_separate_brand_stats_wb import process_separate_brand_stats_wb
from src.logger._logger import logger_msg


async def wb_get_sales(BotDB, target_day):
    print(f'\nНачинаю получать продажи с WB\n')

    wb_core = WBApiSales()

    is_good = True

    for brand, security in WB_API_KEY_LIST.items():

        access_false = filter_brand('wb', brand)

        if access_false:
            continue

        print(f'Начинаю получать продажи с {brand}')

        data_statistic = await wb_core.loop_get_sales(brand, target_day)

        if not data_statistic:
            continue

        sales = len(data_statistic)
        money = 0

        for sale in data_statistic:
            try:
                money += sale['forPay']
            except Exception as es:
                error_ = f'Ошибка при подсчете выручки "{es}"'
                await logger_msg(error_)
                break

        money = round(money, 2)

        # Обработка брендов для отдельной статистики
        if BRANDS_SEPARATE_STATS and data_statistic:
            result = await process_separate_brand_stats_wb(
                data_statistic, BRANDS_SEPARATE_STATS
            )

            if result:
                # Сохраняем статистику по найденным брендам (исключение из общей)
                separate_stats = result.get('separate_stats', {})
                for found_brand, stats in separate_stats.items():
                    sql_data = {
                        'marketplace': 'wb',
                        'brand': found_brand,  # Найденный бренд товара
                        'type': 'order',
                        'count': stats['count'],
                        'money': stats['money'],
                        'date': target_day,
                    }
                    BotDB.check_or_add_static(sql_data)
                    print(f'  -> Отдельная статистика: бренд "{found_brand}", '
                          f'{stats["count"]} продаж, {stats["money"]:.2f} выручки')

                # Вычитаем из основной статистики то, что ушло в отдельные бренды
                total_separate = result.get('total_separate', {})
                sales -= total_separate.get('count', 0)
                money -= total_separate.get('money', 0)

        # Записываем основную статистику по API-ключу (за вычетом найденных брендов)
        if sales > 0 or money > 0:
            sql_data = {
                'marketplace': 'wb',
                'brand': brand,
                'type': 'sale',
                'count': sales,
                'money': money,
                'date': target_day,
            }

            res = BotDB.check_or_add_static(sql_data)

            if not res:
                is_good = False

        print(f'Обработал продажи WB "{brand}"')

    print(f'Обработал все бренды по продажам WB')

    return is_good
