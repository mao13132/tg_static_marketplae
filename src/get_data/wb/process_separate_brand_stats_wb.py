# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from src.logger._logger import logger_msg


async def process_separate_brand_stats_wb(sales_data, brands_config):
    """
    Обработать данные продаж WB и разделить статистику по брендам
    
    В отличие от Ozon, в WB бренд уже содержится напрямую в данных ( поле 'brand' ),
    поэтому не нужно делать дополнительные запросы по SKU.
    
    Args:
        sales_data: Список продаж из WB API (каждая запись содержит поле 'brand')
        brands_config: Словарь брендов для отдельной статистики {brand_lower: brand_name}
        target_day: Дата для записи в статистику
        
    Returns:
        Словарь с накопленной статистикой по найденным брендам:
        {
            'separate_stats': {
                'найденный_бренд_1': {'count': int, 'money': float},
                'найденный_бренд_2': {'count': int, 'money': float},
                ...
            },
            'total_separate': {'count': int, 'money': float}  # сумма для вычитания
        }
        или None если разделение не требуется
    """
    if not sales_data:
        return None

    try:
        # Собираем статистику по каждому найденному бренду из конфигурации
        separate_stats = {}  # {found_brand: {'count': 0, 'money': 0}}

        # Проходим по всем записям продаж и распределяем
        for sale in sales_data:
            try:
                # Получаем бренд товара напрямую из данных
                item_brand = sale.get('brand', '')
                item_brand_lower = item_brand.lower()

                if not item_brand:
                    continue

                # Проверяем есть ли бренд товара в конфигурации (сравниваем по lower)
                if item_brand_lower in brands_config:
                    # Найден бренд который нужно выделить
                    target_brand = item_brand  # Оригинальный регистр для записи

                    if target_brand not in separate_stats:
                        separate_stats[target_brand] = {'count': 0, 'money': 0}

                    # Получаем сумму продажи
                    for_pay = sale.get('forPay', 0)

                    separate_stats[target_brand]['count'] += 1
                    separate_stats[target_brand]['money'] += for_pay

            except Exception as es:
                continue

        if not separate_stats:
            return None

        # Считаем total для вычитания
        total_separate = {'count': 0, 'money': 0}
        for stats in separate_stats.values():
            total_separate['count'] += stats['count']
            total_separate['money'] += stats['money']

        return {
            'separate_stats': separate_stats,
            'total_separate': total_separate
        }

    except Exception as es:
        await logger_msg(f'process_separate_brand_stats_wb: Ошибка обработки брендов "{es}"')
        return None
