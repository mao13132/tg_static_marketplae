# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from src.logger.logger_no_sync import logger_no_sync
from src.logger.telegram.telegram_debug_no_sync import SendlerOneCreate



async def formate_row_week(data_brand):
    try:
        money = data_brand['money']

        old_money = data_brand['old_money']

        sellers = data_brand['sellers']

        old_sellers = data_brand['old_sellers']

        percent_sellers = round(sellers / (old_sellers / 100), 2)

        percent_money = round(money / (old_money / 100), 2)

        icon_count = '🔻' if percent_sellers < 0 else '🔝'

        icon_money = '🔻' if percent_money < 0 else '🔝'

        target_row = f'{money}р / {sellers} шт. ' \
                     f'({percent_money}%{icon_money} / {percent_sellers}%{icon_count})'

    except Exception as es:
        error_ = f'Не могу сформировать текстовую строчку week статистики "{es}"'

        logger_no_sync(error_)

        SendlerOneCreate('').save_text(error_)

        return ''

    return target_row
