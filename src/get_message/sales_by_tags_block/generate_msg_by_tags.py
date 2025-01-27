# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
def generate_msg_by_tags(data, total_data_row_text):
    _msg = '<b>Общие по производствам:</b>\n'

    for tag, data_tag in data.items():

        record_text = ''

        if data_tag['maximal'] and data_tag['total_orders']:
            if data_tag['total_orders'] > data_tag['maximal'][0] or data_tag['total_money'] > data_tag['maximal'][1]:
                record_text = f" 🍾🟢"

        _msg += f'{tag}: {data_tag["data_row_text"]}{record_text}\n'

    _msg += f"Всего заказов по производствам: {total_data_row_text}"

    return _msg
