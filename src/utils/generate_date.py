# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from datetime import datetime, timedelta


def minus_days(day: int):
    """Генерирую вчерашнее число"""

    end_date = (datetime.now() - timedelta(day)).strftime("%Y-%m-%d")

    return end_date
