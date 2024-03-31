# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from src.logger._logger import logger_msg


async def formate_row(now_day, yesterday):
    try:
        count_yesterday, money_yesterday = yesterday

        count_now, money_now = now_day

        if money_now:
            money_now = round(money_now, 2)

        if count_yesterday and money_yesterday and count_now and money_now:

            result_count = count_now - count_yesterday

            money_result = round(money_now - money_yesterday, 2)

            # Вычисляю процент, позавчерашнее делю на 100, результат делю на разницу между днями,
            # тем самым я понимаю сколько это 1 % и после вычисляю сколько процентов в разнице
            count_percent_count = round(result_count / (count_yesterday / 100), 2)

            count_percent_money = round(money_result / (money_yesterday / 100), 2)

        else:
            count_percent_count = 0

            count_percent_money = 0

        icon_count = '🔻' if count_percent_count < 0 else '🔝'

        icon_money = '🔻' if count_percent_money < 0 else '🔝'

        target_row = f'{money_now}р / {count_now} шт. ' \
                     f'({count_percent_money}%{icon_money} / {count_percent_count}%{icon_count})'

    except Exception as es:
        await logger_msg(f'Ошибка при высчитывание значения из строчки "{es}"')

        return 0

    return target_row
