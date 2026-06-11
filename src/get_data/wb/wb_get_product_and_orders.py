# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from settings import WB_API_KEY_LIST, BRANDS_SEPARATE_STATS
from src.api.wb.wb_api_supplier_orders import WBApiSupplierOrders
from src.api.wb.wb_api_get_products import WBApiGetProducts
from src.get_data.wb.process_separate_brand_stats_wb import process_separate_brand_stats_wb
from src.get_message.filter_brand.filter_brand import filter_brand
from src.logger._logger import logger_msg


async def wb_get_product_and_orders(BotDB, target_day):
    """
    Получаем статистику заказов по всем брендам за target_day.
    Используем WBApiSupplierOrders, так как он содержит бренд напрямую в данных.
    """
    print(f'\nНачинаю получать заказы с WB\n')

    is_good = True

    # Перебираем бренды из настроек
    for brand, security in WB_API_KEY_LIST.items():
        # Фильтрация бренда по правилам (например, пропуск некоторых брендов)
        access_false = filter_brand('wb', brand)
        if access_false:
            continue

        # Получаем заказы через Supplier Orders API (содержит бренд в данных)
        print(f'Начинаю получать заказы с {brand}')
        wb_supplier = WBApiSupplierOrders()
        orders_data = await wb_supplier.loop_get_orders_for_date(brand, target_day)

        if not orders_data:
            await logger_msg(f'Не могу получить заказы "{brand}"', push=True)
            continue

        # Считаем общую статистику
        orders = len(orders_data)
        money = 0
        finishedPrice = 0
        priceWithDisc = 0
        totalPrice = 0
        for order in orders_data:
            try:
                money += order.get('totalPrice', 0)
            except Exception:
                continue

            try:
                finishedPrice += order.get('finishedPrice', 0)
            except Exception:
                continue

            try:
                priceWithDisc += order.get('priceWithDisc', 0)
            except Exception:
                continue

            try:
                totalPrice += order.get('totalPrice', 0)
            except Exception:
                continue

        money = round(money, 2)

        # Обработка брендов для отдельной статистики
        if BRANDS_SEPARATE_STATS and orders_data:
            result = await process_separate_brand_stats_wb(
                orders_data, BRANDS_SEPARATE_STATS
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
                          f'{stats["count"]} заказов, {stats["money"]:.2f} выручки')

                # Вычитаем из основной статистики то, что ушло в отдельные бренды
                total_separate = result.get('total_separate', {})
                orders -= total_separate.get('count', 0)
                money -= total_separate.get('money', 0)

        # Записываем основную статистику по API-ключу (за вычетом найденных брендов)
        if orders > 0 or money > 0:
            sql_data = {
                'marketplace': 'wb',
                'brand': brand,
                'type': 'order',
                'count': orders,
                'money': money,
                'date': target_day,
            }

            res = BotDB.check_or_add_static(sql_data)
            if not res:
                is_good = False

        print(f'Обработал заказы WB "{brand}"')

    print(f'Обработал все бренды по заказам WB')
    return is_good
