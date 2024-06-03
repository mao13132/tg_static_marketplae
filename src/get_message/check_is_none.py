# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from src.logger._logger import logger_msg


def check_is_none_from_tuple(in_tuple):
    try:

        one_value, two_value = in_tuple

        if one_value is None:
            one_value = 0

        if two_value is None:
            two_value = 0

    except Exception as es:
        logger_msg(f'Не могу проверить значения на None "{es}"')

        return in_tuple

    return (one_value, two_value)
