# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from src.api.ozon.ozon_api_product_info import OzonApiProductInfo
from src.logger._logger import logger_msg


async def process_separate_brand_stats(security, original_brand, rows, brands_config, target_day):
    """
    Обработать товары и разделить статистику по брендам
    
    Args:
        security: Параметры безопасности (client_id, api_key)
        original_brand: Название бренда по API-ключу
        rows: Список строк с данными о заказах (result.data)
        brands_config: Словарь брендов для отдельной статистики {brand_lower: brand_name}
        target_day: Дата для записи в статистику
        
    Returns:
        Словарь с накопленной статистикой по найденным брендам:
        {
            'separate_stats': {
                'найденный_бренд_1': {'orders': int, 'profit': float, 'count': int},
                'найденный_бренд_2': {'orders': int, 'profit': float, 'count': int},
                ...
            },
            'total_separate': {'orders': int, 'profit': float}  # сумма для вычитания
        }
        или None если разделение не требуется
    """
    if not rows:
        return None

    try:
        # Собираем уникальные SKU из rows
        # Структура: dimensions = [{'id': '3855101605', 'name': '...'}, {'id': '2026-06-08', 'name': ''}]
        # Первый элемент - товар (SKU Ozon), второй - дата
        unique_skus = set()
        for row in rows:
            try:
                dimensions = row.get('dimensions', [])
                if dimensions and len(dimensions) >= 1:
                    # Первый элемент - товар (SKU Ozon)
                    sku = dimensions[0].get('id', '')
                    if sku:
                        unique_skus.add(sku)
            except:
                continue

        if not unique_skus:
            return None

        # Получаем информацию о брендах для всех SKU
        sku_list = list(unique_skus)
        ozon_product_info = OzonApiProductInfo()
        brand_mapping = await ozon_product_info.loop_get_product_attributes(
            original_brand, security, sku_list
        )

        if not brand_mapping:
            return None

        # Собираем статистику по каждому найденному бренду из конфигурации
        separate_stats = {}  # {found_brand: {'orders': 0, 'profit': 0, 'count': 0}}

        # Проходим по всем строкам и распределяем
        for row in rows:
            try:
                metrics = row.get('metrics', [])
                if len(metrics) < 2:
                    continue

                row_orders = int(metrics[0])
                row_profit = float(metrics[1])

                dimensions = row.get('dimensions', [])
                if not dimensions or len(dimensions) < 1:
                    continue

                # Первый элемент - товар (SKU Ozon)
                sku = dimensions[0].get('id', '')

                if not sku:
                    continue

                # Проверяем есть ли бренд товара в конфигурации (сравниваем по lower)
                item_brand_lower = brand_mapping.get(sku, '').lower()
                item_brand_original = brand_mapping.get(sku, '')

                if item_brand_lower in brands_config:
                    # Найден бренд который нужно выделить
                    target_brand = item_brand_original

                    if target_brand not in separate_stats:
                        separate_stats[target_brand] = {'orders': 0, 'profit': 0, 'count': 0}

                    separate_stats[target_brand]['orders'] += row_orders
                    separate_stats[target_brand]['profit'] += row_profit
                    separate_stats[target_brand]['count'] += 1

            except Exception as es:
                continue

        if not separate_stats:
            return None

        # Считаем total для вычитания
        total_separate = {'orders': 0, 'profit': 0}
        for stats in separate_stats.values():
            total_separate['orders'] += stats['orders']
            total_separate['profit'] += stats['profit']

        return {
            'separate_stats': separate_stats,
            'total_separate': total_separate
        }

    except Exception as es:
        await logger_msg(f'process_separate_brand_stats: Ошибка обработки брендов "{es}"')
        return None
