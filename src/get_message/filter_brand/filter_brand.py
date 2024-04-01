# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from settings import STOP_BRAND_FILTER


def filter_brand(marketplace, brand):
    for in_filter in STOP_BRAND_FILTER:
        if marketplace == in_filter['marketpalce'] and brand == in_filter['brand']:
            return True

    return False
