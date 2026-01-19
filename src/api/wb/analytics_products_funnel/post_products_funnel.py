# ---------------------------------------------
# Program by @developer_telegrams
#
# Задача файла:
# - Выполняет HTTP POST к "sales-funnel/products".
# - Этот слой отвечает за сетевое взаимодействие:
#   собирает URL, заголовки, тело запроса и возвращает ответ/сигналы ретрая.
# ---------------------------------------------
import aiohttp

from src.api.wb.wb_api_core import WBApiCore
from src.logger._logger import logger_msg


async def post_products_funnel(api_key, nmids_chunk, selected_start, selected_end, past_start=None, past_end=None, limit=None, offset=0):
    # api_key: ключ авторизации для заголовка Authorization
    # nmids_chunk: список артикулов (<= 20 по нашей стратегии)
    # selected_start, selected_end: даты периода (YYYY-MM-DD)
    # past_start, past_end: опционально — период для сравнения (YYYY-MM-DD)
    # limit: ограничение числа карточек в ответе (по умолчанию — длина пачки)
    # offset: смещение для пагинации
    #
    # Возвращает:
    # - JSON (dict) при статусе 200
    # - '-1' при временной ошибке (429/503) — вызывающий код выполнит ретрай
    # - False при фатальной ошибке (401/прочее) — вызывающий код прекратит работу

    core = WBApiCore()  # Базовые настройки и URL

    # Конечный URL для вызова продукта аналитики
    url = core.new_analitic_url + 'api/analytics/v3/sales-funnel/products'

    # Заголовки — обязательный Authorization
    headers = {
        'Content-Type': 'application/json',
        'Authorization': api_key,
    }

    # Формируем тело запроса по спецификации
    payload = {
        'selectedPeriod': {
            'start': selected_start,
            'end': selected_end,
        },
        'nmIds': nmids_chunk or [],
        'brandNames': [],
        'subjectIds': [],
        'tagIds': [],
        'skipDeletedNm': True,
        'limit': limit if limit is not None else max(len(nmids_chunk or []), 1),
        'offset': offset,
    }

    # Если задан период сравнения — добавляем его
    if past_start and past_end:
        payload['pastPeriod'] = {
            'start': past_start,
            'end': past_end,
        }

    try:
        # Создаём HTTP‑сессию с базовым таймаутом
        async with aiohttp.ClientSession(timeout=core.session_timeout) as session:
            # Выполняем POST
            async with session.post(
                url,
                timeout=aiohttp.ClientTimeout(total=60),
                headers=headers,
                json=payload,
            ) as res:
                # Успех — возвращаем JSON
                if res.status == 200:
                    return await res.json()

                # Пытаемся прочитать тело ошибки для диагностики
                try:
                    error_body = await res.json()
                except Exception:
                    error_body = {'detail': f'HTTP {res.status}'}

                # Достаём сообщение
                msg = (
                    (error_body.get('detail') if isinstance(error_body, dict) else None)
                    or (error_body.get('message') if isinstance(error_body, dict) else None)
                    or str(error_body)
                )

                # Временные ошибки — ретрай
                if res.status in (429, 503):
                    await logger_msg(
                        f'WB Products Funnel: слишком много запросов или недоступно, ретрай: "{msg}"'
                    )
                    return '-1'

                # Неавторизован — сообщаем и прекращаем
                if res.status == 401:
                    await logger_msg(
                        f'WB Products Funnel: не авторизован, проверьте ключ: "{msg}"',
                        push=True,
                    )
                    return False

                # Прочее — фатальная ошибка
                await logger_msg(f'WB Products Funnel: ошибка запроса "{msg}"', push=True)
                return False

    except Exception as es:
        # Исключение — логируем и предлагаем ретрай
        await logger_msg(f'WB Products Funnel: исключение "{es}"')
        return '-1'

