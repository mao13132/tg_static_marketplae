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

        _msg += f'{tag}: {data_tag["data_row_text"]}\n'

    _msg += f"Всего заказов по производствам: {total_data_row_text}"

    return _msg
