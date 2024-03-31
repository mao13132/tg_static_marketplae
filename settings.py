import os

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), 'src', '.env'))

ADMIN = ['1422194909']

TOKEN = os.getenv('TOKEN')

LOGO = r'src/telegram/media/logo.png'

START_MESSAGE = '⚙️Админ панель'

MARKETPLACE = ['ozon', 'wb']

NAME_BRAND = {
    3: 'GreenFormula',
    4: 'Guru',
    0: 'Benerich',
    6: 'Kronly',
    7: 'Little Dreams',
    8: 'Militon',
    5: 'iGGi',
    1: 'CaptainOil',
    2: 'Ergonom Office',
    9: 'Udnet Retail',
}

BRANDS_BY_DIRECTION = {
    "Продукты питания": [NAME_BRAND[3], NAME_BRAND[4], NAME_BRAND[0]],
    "Кресла": [NAME_BRAND[2], NAME_BRAND[9]],
}

OZON_API_KEY_LIST = {
    NAME_BRAND[0]: [os.getenv('CLIENT_ID1'), os.getenv('OZON_API_KEY1')],
    NAME_BRAND[1]: [os.getenv('CLIENT_ID2'), os.getenv('OZON_API_KEY2')],
    NAME_BRAND[2]: [os.getenv('CLIENT_ID3'), os.getenv('OZON_API_KEY3')],
    NAME_BRAND[3]: [os.getenv('CLIENT_ID4'), os.getenv('OZON_API_KEY4')],
    NAME_BRAND[4]: [os.getenv('CLIENT_ID5'), os.getenv('OZON_API_KEY5')],
    NAME_BRAND[5]: [os.getenv('CLIENT_ID6'), os.getenv('OZON_API_KEY6')],
    NAME_BRAND[6]: [os.getenv('CLIENT_ID7'), os.getenv('OZON_API_KEY7')],
    NAME_BRAND[7]: [os.getenv('CLIENT_ID8'), os.getenv('OZON_API_KEY8')],
    NAME_BRAND[8]: [os.getenv('CLIENT_ID9'), os.getenv('OZON_API_KEY9')],
    NAME_BRAND[9]: [os.getenv('CLIENT_ID10'), os.getenv('OZON_API_KEY10')],
}

WB_API_KEY_LIST = {
    NAME_BRAND[3]: [os.getenv('api_key'), os.getenv('api_key2')],
    NAME_BRAND[4]: [os.getenv('api_key_guru'), os.getenv('api_key_guru2')],
    NAME_BRAND[6]: [os.getenv('api_key_po'), os.getenv('api_key_po2')],
    NAME_BRAND[7]: [os.getenv('api_key_shelepina'), os.getenv('api_key_shelepina2')],
    NAME_BRAND[5]: [os.getenv('api_key_iggi'), os.getenv('api_key_iggi2')],
    NAME_BRAND[0]: [os.getenv('api_key_benerich'), os.getenv('api_key_benerich2')],
    NAME_BRAND[9]: [os.getenv('api_key_dealex'), os.getenv('api_key_dealex2')]
}
