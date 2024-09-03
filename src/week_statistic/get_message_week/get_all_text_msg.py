# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from src.week_statistic.get_message_week._formate_row import formate_row_week
from src.week_statistic.get_message_week._search_category_name import search_category_name


async def get_all_text_msg(data_week):
    _msg = '%one_row%\n'

    for brand, data_brand in data_week.items():
        if type(data_brand) != dict:
            continue

        one_row = f"💰<b>Прибыль за неделю: ({data_brand['start_date'][:-5]} - {data_brand['end_date'][:-5]})</b>"

        if '%one_row%' in _msg:
            _msg = _msg.replace('%one_row%', one_row)

        text_row = await formate_row_week(data_brand)

        if not text_row:
            continue

        category_name = await search_category_name(brand)

        _msg += f'{category_name}: {text_row}\n'

        continue

    return _msg


if __name__ == '__main__':
    from temp.temp_week import data
    import asyncio

    res_ = asyncio.run(get_all_text_msg(data))

    print()
