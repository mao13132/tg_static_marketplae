# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
import time

import aiohttp

from src.api.ozon.get_api_key import get_api_key
from src.logger._logger import logger_msg
from src.api.ozon.ozon_api_core import OzonApiCore


class OzonApiProductInfo(OzonApiCore):
    """Класс для получения информации о товарах Ozon"""

    async def get_product_attributes(self, client_id, api_key, sku_list):
        """Получить атрибуты товаров по SKU Ozon
        
        Args:
            client_id: ID клиента
            api_key: API ключ
            sku_list: список SKU товаров Ozon
            
        Returns:
            Список товаров с их атрибутами включая brand
        """
        url = self.url_seller + f'v4/product/info/attributes'

        header_ = {
            'Content-Type': 'application/json',
            'Client-Id': client_id,
            'Api-Key': api_key
        }

        data_ = {
            "filter": {
                "sku": sku_list
            },
            "limit": 1000
        }

        try:
            async with aiohttp.ClientSession(timeout=self.session_timeout) as session:
                async with session.post(url,
                                        timeout=aiohttp.ClientTimeout(total=60),
                                        headers=header_,
                                        json=data_) as resul:
                    response = await resul.json()

                    if resul.status == 200 and not response:
                        await logger_msg(f'OZON get_product_attributes: Нулевой ответ от серверов')
                        return []

                    return response.get('result', [])

        except Exception as es:
            await logger_msg(f'OZON get_product_attributes: Ошибка при получении атрибутов товаров "{es}"')
            return []

    async def loop_get_product_attributes(self, name_sheet, security, sku_list, max_ids=1000):
        """Получить атрибуты товаров по SKU с обработкой пагинации
        
        Args:
            name_sheet: Название кабинета для логов
            security: Параметры безопасности (client_id, api_key)
            sku_list: Список SKU Ozon
            max_ids: Максимум ID за один запрос (по умолчанию 1000)
            
        Returns:
            Словарь {sku: brand} для всех товаров
        """
        client_id, api_key = await get_api_key(security)

        if not client_id:
            return {}

        result_brands = {}
        last_id = None

        # Разбиваем на чанки по max_ids SKU
        while True:
            chunk = sku_list[:max_ids] if not last_id else None
            
            for _try in range(self.count_try):
                if last_id:
                    # Пагинация - используем last_id
                    data_ = {
                        "filter": {},
                        "last_id": last_id,
                        "limit": max_ids
                    }
                elif chunk:
                    # Первый запрос - фильтр по SKU
                    data_ = {
                        "filter": {
                            "sku": sku_list[:max_ids]
                        },
                        "limit": max_ids
                    }
                else:
                    break

                url = self.url_seller + f'v4/product/info/attributes'
                header_ = {
                    'Content-Type': 'application/json',
                    'Client-Id': client_id,
                    'Api-Key': api_key
                }

                try:
                    async with aiohttp.ClientSession(timeout=self.session_timeout) as session:
                        async with session.post(url,
                                                timeout=aiohttp.ClientTimeout(total=60),
                                                headers=header_,
                                                json=data_) as resul:
                            response = await resul.json()

                            if not response or resul.status != 200:
                                time.sleep(self.time_try)
                                continue

                            items = response.get('result', [])
                            last_id = response.get('last_id')

                            if not items:
                                break

                            # Извлекаем brand из атрибутов каждого товара
                            for item in items:
                                sku = str(item.get('sku', ''))
                                brand = self._extract_brand_from_attributes(item.get('attributes', []))
                                if sku and brand:
                                    result_brands[sku] = brand

                            # Если нет last_id или получено меньше чем limit - это конец
                            if not last_id or len(items) < max_ids:
                                return result_brands

                except Exception as es:
                    await logger_msg(f'OZON loop_get_product_attributes: Ошибка итерации "{es}"')
                    time.sleep(self.time_try)
                    continue

                break

            if not last_id:
                break

            time.sleep(0.5)  # Небольшая пауза между запросами

        return result_brands

    def _extract_brand_from_attributes(self, attributes):
        """Извлечь бренд из массива атрибутов товара
        
        Brand может быть в атрибуте с id=85 (категория "Brand")
        или в атрибуте с dictionary_value_id указывающим на справочник брендов
        """
        if not attributes:
            return ''

        # Ищем атрибут с id=85 (категория "Brand")
        for attr in attributes:
            if attr.get('id') == 85:
                # Нашли атрибут бренда
                values = attr.get('values', [])
                if values and len(values) > 0:
                    # Если есть dictionary_value_id - нужно искать в справочнике
                    # Но пока возвращаем значение напрямую
                    return values[0].get('value', '')
        
        # Альтернативный поиск - ищем любой атрибут содержащий "brand" в имени
        for attr in attributes:
            attr_values = attr.get('values', [])
            if attr_values:
                value = attr_values[0].get('value', '')
                # Проверяем если value выглядит как бренд (не число, не boolean)
                if value and not value.lower() in ['true', 'false'] and len(value) > 1:
                    # Пропускаем числовые значения
                    try:
                        float(value)
                        continue
                    except:
                        pass
                    return value

        return ''
