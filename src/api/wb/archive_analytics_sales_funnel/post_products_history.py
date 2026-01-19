# ---------------------------------------------
# Program by @developer_telegrams
#
# Задача файла:
# - Выполняет HTTP POST к "sales-funnel/products/history".
# - Этот слой отвечает только за сетевое взаимодействие:
#   собирает URL, заголовки, тело запроса и возвращает ответ или сигнал о ретрае/ошибке.
# ---------------------------------------------
import aiohttp

from src.api.wb.wb_api_core import WBApiCore
from src.logger._logger import logger_msg


async def post_products_history(api_key, nmids_chunk, start_date, end_date):
    # api_key: ключ авторизации для заголовка Authorization
    # nmids_chunk: список артикулов (<= 20) для одного запроса
    # start_date, end_date: даты периода (строки в формате YYYY-MM-DD)
    # Возвращает:
    # - JSON (list) при статусе 200
    # - '-1' при временной ошибке (429/503) — вызывающий код выполнит ретрай
    # - False при фатальной ошибке (401/прочее) — вызывающий код прекратит работу

    core = WBApiCore()  # Берем базовые настройки и базовый URL

    # Собираем конечный URL для вызова метода из новой аналитики
    url = core.new_analitic_url + 'api/analytics/v3/sales-funnel/products/history'

    # Формируем заголовки: обязательно передаем Authorization
    headers = {
        'Content-Type': 'application/json',
        'Authorization': api_key,
    }

    # Формируем тело запроса по спецификации:
    # - selectedPeriod: { start, end }
    # - nmIds: список артикулов (от 1 до 20)
    # - skipDeletedNm: True (скрыть удаленные)
    # - aggregationLevel: "day" (агрегация по дням)
    payload = {
        'selectedPeriod': {
            'start': start_date,
            'end': end_date,
        },
        'nmIds': nmids_chunk,
        'skipDeletedNm': True,
        'aggregationLevel': 'day',
    }

    try:
        # Создаем HTTP-сессию с таймаутом из ядра
        async with aiohttp.ClientSession(timeout=core.session_timeout) as session:
            # Выполняем POST с явным таймаутом операции (60 сек) и нашим телом запроса
            async with session.post(
                url,
                timeout=aiohttp.ClientTimeout(total=60),
                headers=headers,
                json=payload,
            ) as res:
                # Успешный ответ — возвращаем JSON как есть
                if res.status == 200:
                    return await res.json()

                # Пытаемся прочитать тело ошибки для диагностического сообщения
                try:
                    error_body = await res.json()
                except Exception:
                    error_body = {'detail': f'HTTP {res.status}'}

                # Достаём человеко-читаемое сообщение
                msg = (
                    (error_body.get('detail') if isinstance(error_body, dict) else None)
                    or (error_body.get('message') if isinstance(error_body, dict) else None)
                    or str(error_body)
                )

                # 429/503 — временные ситуации, просим повторить
                if res.status in (429, 503):
                    await logger_msg(
                        f'WB Sales Funnel: слишком много запросов или недоступно, ретрай: "{msg}"'
                    )
                    return '-1'

                # 401 — неавторизован (например, пустой заголовок Authorization)
                if res.status == 401:
                    await logger_msg(
                        f'WB Sales Funnel: не авторизован, проверьте ключ: "{msg}"',
                        push=True,
                    )
                    return False

                # Прочие ошибки — считаем фатальными
                await logger_msg(f'WB Sales Funnel: ошибка запроса "{msg}"', push=True)
                return False

    except Exception as es:
        # Любая непредвиденная ошибка — логируем и предлагаем ретрай
        await logger_msg(f'WB Sales Funnel: исключение "{es}"')
        return '-1'

