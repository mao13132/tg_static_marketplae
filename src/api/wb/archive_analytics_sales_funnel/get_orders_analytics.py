# ---------------------------------------------
# Program by @developer_telegrams
#
# Задача файла:
# - Оркестрация получения "заказов" из Sales Funnel API.
# - На вход: бренд, список артикулов, дата (target_day).
# - Действия:
#   1) Разбивает артикулы на пачки по 20.
#   2) Для каждой пачки вызывает POST products/history.
#   3) Собирает ответы и приводит к формату истории заказов,
#      совместимому с calculation_orders.py.
# ---------------------------------------------
import time

from src.api.wb.get_api_key import wb_get_api_key
from src.api.wb.wb_api_core import WBApiCore
from src.api.wb.archive_analytics_sales_funnel.chunk_nmids import chunk_nmids, CHUNK_SIZE
from src.api.wb.archive_analytics_sales_funnel.post_products_history import post_products_history
from src.api.wb.archive_analytics_sales_funnel.format_analytics_orders import format_analytics_orders_to_history
from src.logger._logger import logger_msg


async def get_orders_from_analytics_by_articles(brand, article_list, target_day):
    # brand: название бренда (ключ для получения API-ключа)
    # article_list: список артикулов (nmIDs), которые нужно обработать
    # target_day: дата-строка YYYY-MM-DD, за которую берём статистику (start=end)
    #
    # Возвращает:
    # - список объектов вида:
    #   [{'nmID': <int>, 'history': [{'ordersCount': <int>, 'ordersSumRub': <float> }]}]
    # - False при фатальной ошибке

    core = WBApiCore()  # Берем параметры ретраев/таймаутов и др.

    # Ключ для доступа к аналитике. Используем индекс 0 как для статистики/продаж.
    api_key = await wb_get_api_key(brand, 0)
    if not api_key:
        return False

    # Разбиваем артикулы на пачки по 20 для соответствия лимиту API
    batches = chunk_nmids(article_list, size=CHUNK_SIZE)
    if not batches:
        # Если нет артикулов — возвращаем пустой набор
        return []

    all_responses = []  # Здесь соберём ответы по всем пачкам

    # Идем по пачкам последовательно, соблюдая ретраи и паузы
    for batch in batches:
        # Несколько попыток для каждой пачки
        ok = False
        for _try in range(core.count_try):
            # Запрашиваем историю для текущей пачки на указанный день
            response = await post_products_history(api_key, batch, target_day, target_day)

            # '-1' — временная ошибка, ждём и пробуем ещё раз
            if response == '-1':
                time.sleep(core.time_try)
                continue

            # False — фатальная ошибка, прекращаем работу
            if response is False:
                await logger_msg(f'WB Sales Funnel: ошибка при запросе пачки артикулов у "{brand}"', push=True)
                return False

            # Всё хорошо — сохраняем ответ и выходим из цикла ретрая
            all_responses.append(response or [])
            ok = True
            break

        # Если все попытки исчерпаны и успеха нет — логируем и прекращаем
        if not ok:
            await logger_msg(f'WB Sales Funnel: исчерпаны попытки для пачки у "{brand}"', push=True)
            return False

    # Все ответы собраны — приводим к целевому формату истории заказов
    formatted = format_analytics_orders_to_history(all_responses, article_list)
    return formatted

