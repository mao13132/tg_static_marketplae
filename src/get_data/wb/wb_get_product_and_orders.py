# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from settings import WB_API_KEY_LIST
from src.api.wb.calculation_orders import calculation_orders
from src.api.wb.wb_api_get_products import WBApiGetProducts
from src.api.wb.analytics_products_funnel.get_orders_products_funnel import get_orders_from_products_funnel_by_articles
from src.get_message.filter_brand.filter_brand import filter_brand
from src.logger._logger import logger_msg


async def wb_get_product_and_orders(BotDB, target_day):
    # Начало процесса: получаем статистику заказов по всем брендам за target_day через новую аналитику
    print(f'\nНачинаю получать заказы с WB\n')

    is_good = True

    # Перебираем бренды из настроек
    for brand, security in WB_API_KEY_LIST.items():
        # Фильтрация бренда по правилам (например, пропуск некоторых брендов)
        access_false = filter_brand('wb', brand)
        if access_false:
            continue

        # Шаг 1: получаем список продуктов бренда
        print(f'Начинаю получать продукты с {brand}')
        products = await WBApiGetProducts().loop_get_products(brand)

        if not products:
            await logger_msg(f'Не могу получить список продуктов "{brand}"', push=True)
            continue

        # Достаём артикулы (nmID) из списка продуктов
        article_list = [product['nmID'] for product in products]

        # from src.api.wb.archive_analytics_sales_funnel.get_orders_analytics import get_orders_from_analytics_by_articles
        # # Шаг 2: для этих артикулов получаем историю заказов из Sales Funnel (Analytics)
        # print(f'Начинаю получать заказы (Analytics) с {brand}')
        # data_statistic = await get_orders_from_analytics_by_articles(brand, article_list, target_day)

        # Шаг 2: для этих артикулов получаем агрегированную статистику заказов через Sales Funnel (products)
        print(f'Начинаю получать заказы (Products Funnel) с {brand}')
        data_statistic = await get_orders_from_products_funnel_by_articles(brand, article_list, target_day)

        # Если получили и смогли привести к целевому формату — считаем общие заказы и сумму
        if data_statistic:
            orders, money = await calculation_orders(data_statistic, brand)
        else:
            money = 0
            orders = 0

        # Формируем запись для БД
        sql_data = {
            'marketplace': 'wb',
            'brand': brand,
            'type': 'order',
            'count': orders,
            'money': money,
            'date': target_day,
        }

        # Сохраняем результат в БД
        res = BotDB.check_or_add_static(sql_data)
        if not res:
            is_good = False

        print(f'Обработал заказы WB "{brand}"')

    print(f'Обработал все бренды по продажам WB')
    return is_good
