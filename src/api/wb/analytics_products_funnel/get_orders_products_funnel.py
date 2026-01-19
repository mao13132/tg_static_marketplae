# ---------------------------------------------
# Program by @developer_telegrams
#
# Задача файла:
# - Оркестрация получения "заказов" через Sales Funnel / products.
# - На вход: бренд, список артикулов, дата (target_day).
# - Действия:
#   1) Разбивает артикулы на пачки по 20.
#   2) Для каждой пачки вызывает POST products.
#   3) Собирает ответы и приводит к формату истории заказов,
#      совместимому с calculation_orders.py.
# ---------------------------------------------
import time

from src.api.wb.get_api_key import wb_get_api_key
from src.api.wb.wb_api_core import WBApiCore
from src.api.wb.analytics_products_funnel.chunk_nmids import chunk_nmids, CHUNK_SIZE
from src.api.wb.analytics_products_funnel.post_products_funnel import post_products_funnel
from src.api.wb.analytics_products_funnel.format_products_orders import format_products_orders_to_history
from src.logger._logger import logger_msg


async def get_orders_from_products_funnel_by_articles(brand, article_list, target_day):
    # brand: название бренда
    # article_list: список артикулов (nmIDs), которые нужно обработать
    # target_day: дата-строка YYYY-MM-DD (используем как selectedPeriod: start=end)
    #
    # Возвращает:
    # - список объектов вида:
    #   [{'nmID': <int>, 'history': [{'ordersCount': <int>, 'ordersSumRub': <float> }]}]
    # - False при фатальной ошибке

    core = WBApiCore()

    api_key = await wb_get_api_key(brand, 0)
    if not api_key:
        return False

    batches = chunk_nmids(article_list, size=CHUNK_SIZE)
    if not batches:
        return []

    all_responses = []

    for batch in batches:
        ok = False
        for _try in range(core.count_try):
            response = await post_products_funnel(
                api_key=api_key,
                nmids_chunk=batch,
                selected_start=target_day,
                selected_end=target_day,
                past_start=None,
                past_end=None,
                limit=len(batch),
                offset=0,
            )

            if response == '-1':
                time.sleep(core.time_try)
                continue

            if response is False:
                await logger_msg(f'WB Products Funnel: ошибка при запросе пачки артикулов у "{brand}"', push=True)
                return False

            all_responses.append(response or {})
            ok = True
            break

        if not ok:
            await logger_msg(f'WB Products Funnel: исчерпаны попытки для пачки у "{brand}"', push=True)
            return False

    formatted = format_products_orders_to_history(all_responses, article_list)
    return formatted

