# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from settings import BRANDS_BY_DIRECTION


async def search_category_name(brand):
    for category_name, brand_list in BRANDS_BY_DIRECTION.items():
        if brand in brand_list:
            return category_name

    return brand
