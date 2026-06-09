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


async def process_separate_brand_stats_for_sales(security, original_brand, operations, brands_config, target_day):
    """
    Обработать операции продаж и разделить статистику по брендам
    
    Args:
        security: Параметры безопасности (client_id, api_key)
        original_brand: Название бренда по API-ключу
        operations: Список операций из v3/finance/transaction/list
        brands_config: Словарь брендов для отдельной статистики {brand_lower: brand_name}
        target_day: Дата для записи в статистику
        
    Returns:
        Словарь с накопленной статистикой по найденным брендам:
        {
            'separate_stats': {
                'найденный_бренд_1': {'operations': int, 'money': float, 'count': int},
                'найденный_бренд_2': {'operations': int, 'money': float, 'count': int},
                ...
            },
            'total_separate': {'operations': int, 'money': float}  # сумма для вычитания
        }
        или None если разделение не требуется
    """
    if not operations:
        return None

    try:
        # Собираем уникальные SKU из operations
        # Структура операции: {'operation_type': ..., 'items': [...], ...}
        # Внутри items может быть sku или product_id
        unique_skus = set()
        for op in operations:
            try:
                items = op.get('items', [])
                for item in items:
                    # Пробуем разные поля для идентификатора товара
                    sku = item.get('sku') or item.get('product_id') or item.get('offer_id', '')
                    if sku:
                        unique_skus.add(str(sku))
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
        separate_stats = {}  # {found_brand: {'operations': 0, 'money': 0, 'count': 0}}

        # Проходим по всем операциям и распределяем
        for op in operations:
            try:
                # Получаем тип операции и сумму начислений
                operation_type = op.get('operation_type', '')
                
                # Для canceled операций берем отрицательные значения
                if 'Canceled' in operation_type:
                    # canceled операции имеют отрицательные суммы
                    accruals = op.get('accruals_for_sale', 0)
                    if accruals and accruals < 0:
                        accruals = abs(accruals)  # берем абсолютное значение для статистики
                    else:
                        continue  # пропускаем если нет начислений или они положительные
                else:
                    accruals = op.get('accruals_for_sale', 0)
                    if not accruals or accruals <= 0:
                        continue

                items = op.get('items', [])
                if not items:
                    continue

                # Обрабатываем каждый товар в операции
                for item in items:
                    sku = str(item.get('sku') or item.get('product_id') or item.get('offer_id', ''))
                    if not sku:
                        continue

                    # Проверяем есть ли бренд товара в конфигурации (сравниваем по lower)
                    item_brand_lower = brand_mapping.get(sku, '').lower()
                    item_brand_original = brand_mapping.get(sku, '')

                    if item_brand_lower in brands_config:
                        # Найден бренд который нужно выделить
                        target_brand = item_brand_original

                        if target_brand not in separate_stats:
                            separate_stats[target_brand] = {'operations': 0, 'money': 0, 'count': 0}

                        # Считаем количество товаров в операции
                        quantity = item.get('quantity', 1)
                        
                        separate_stats[target_brand]['operations'] += 1
                        separate_stats[target_brand]['money'] += accruals * quantity
                        separate_stats[target_brand]['count'] += quantity

            except Exception as es:
                continue

        if not separate_stats:
            return None

        # Считаем total для вычитания
        total_separate = {'operations': 0, 'money': 0}
        for stats in separate_stats.values():
            total_separate['operations'] += stats['operations']
            total_separate['money'] += stats['money']

        return {
            'separate_stats': separate_stats,
            'total_separate': total_separate
        }

    except Exception as es:
        await logger_msg(f'process_separate_brand_stats_for_sales: Ошибка обработки брендов "{es}"')
        return None