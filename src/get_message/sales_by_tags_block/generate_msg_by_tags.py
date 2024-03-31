# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
def generate_msg_by_tags(data):
    _msg = 'Общие по направлениям:\n'

    for tag, data_tag in data.items():

        _msg += f'{tag}: {data_tag["data_row_text"]}\n'

    return _msg
