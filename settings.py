import os

from dotenv import load_dotenv

from src.utils.generate_date import minus_days

program_dir = os.path.dirname(__file__)

load_dotenv(os.path.join(os.path.dirname(__file__), 'src', '.env'))

TOKEN = os.getenv('TOKEN')

LOGO = r'src/telegram/media/logo.png'

START_MESSAGE = '⚙️Админ панель'

TARGET_DAY = minus_days(1)

ANALYST_DAY = minus_days(2)

MARKETPLACE = ['ozon', 'wb']

NAME_BRAND = {
    13: 'Kronly',
    14: 'Kronly Agent',
    15: 'Spets ЗБХ',
    16: 'Spets ЗФП',
    17: 'Spets Контракт',
    18: 'Spets Юникорн',




    # 3: 'GreenFormula',
    # 4: 'Guru',
    # 0: 'Benerich',
    # # 7: 'Little Dreams',
    # 8: 'Militon',
    #
    # 6: 'Kronly',  # это ФДИ
    #
    # 10: 'Spets',
    # 11: 'Слиппи',
    # 12: 'Spets Nutri care'
}

OZON_API_KEY_LIST = {
    NAME_BRAND[13]: [os.getenv('CLIENT_ID13'), os.getenv('OZON_API_KEY13')],
    NAME_BRAND[15]: [os.getenv('CLIENT_ID15'), os.getenv('OZON_API_KEY15')],
    NAME_BRAND[16]: [os.getenv('CLIENT_ID16'), os.getenv('OZON_API_KEY16')],
    NAME_BRAND[17]: [os.getenv('CLIENT_ID17'), os.getenv('OZON_API_KEY17')],
    NAME_BRAND[18]: [os.getenv('CLIENT_ID18'), os.getenv('OZON_API_KEY18')],

    # NAME_BRAND[0]: [os.getenv('CLIENT_ID1'), os.getenv('OZON_API_KEY1')],
    # NAME_BRAND[3]: [os.getenv('CLIENT_ID4'), os.getenv('OZON_API_KEY4')],
    # NAME_BRAND[4]: [os.getenv('CLIENT_ID5'), os.getenv('OZON_API_KEY5')],
    # NAME_BRAND[6]: [os.getenv('CLIENT_ID7'), os.getenv('OZON_API_KEY7')],
    # # NAME_BRAND[7]: [os.getenv('CLIENT_ID8'), os.getenv('OZON_API_KEY8')],
    # NAME_BRAND[8]: [os.getenv('CLIENT_ID9'), os.getenv('OZON_API_KEY9')],
    # NAME_BRAND[10]: [os.getenv('CLIENT_ID10'), os.getenv('OZON_API_KEY10')],
    # NAME_BRAND[11]: [os.getenv('CLIENT_ID_SLIPY'), os.getenv('OZON_API_SLIPY')],
    # NAME_BRAND[12]: [os.getenv('CLIENT_ID_NUTRI'), os.getenv('OZON_API_NUTRI')],
}

WB_API_KEY_LIST = {
    NAME_BRAND[13]: [os.getenv('api_key13'), os.getenv('api_key13')],
    NAME_BRAND[14]: [os.getenv('api_key14'), os.getenv('api_key14')],
    NAME_BRAND[15]: [os.getenv('api_key15'), os.getenv('api_key15')],
    NAME_BRAND[16]: [os.getenv('api_key16'), os.getenv('api_key16')],
    NAME_BRAND[17]: [os.getenv('api_key17'), os.getenv('api_key17')],
    NAME_BRAND[18]: [os.getenv('api_key18'), os.getenv('api_key18')],




    # NAME_BRAND[3]: [os.getenv('api_key'), os.getenv('api_key2')],
    # NAME_BRAND[6]: [os.getenv('api_key_fdi'), os.getenv('api_key_fdi2')],
    # NAME_BRAND[7]: [os.getenv('api_key_shelepina'), os.getenv('api_key_shelepina2')],
    # NAME_BRAND[10]: [os.getenv('api_key_spets'), os.getenv('api_key_spets2')],
    # NAME_BRAND[11]: [os.getenv('API_KEY_WB_SLIPY'), os.getenv('API_KEY_WB_SLIPY')],
    # NAME_BRAND[12]: [os.getenv('API_KEY_WB_NUTRI'), os.getenv('API_KEY_WB_NUTRI')],
}


STOP_BRAND_FILTER = [
    {
        'marketpalce': 'ozon',
        'brand': NAME_BRAND[14]
    },
    # {
    #     'marketpalce': 'wb',
    #     'brand': NAME_BRAND[4]
    # },
    # {
    #     'marketpalce': 'wb',
    #     'brand': NAME_BRAND[3]
    # },
    # {
    #     'marketpalce': 'wb',
    #     'brand': NAME_BRAND[0]
    # },
    # {
    #     'marketpalce': 'wb',
    #     'brand': NAME_BRAND[8]
    # },
    # {
    #     'marketpalce': 'ozon',
    #     'brand': NAME_BRAND[0]
    # },
    # {
    #     'marketpalce': 'ozon',
    #     'brand': NAME_BRAND[4]
    # },
    # {
    #     'marketpalce': 'ozon',
    #     'brand': NAME_BRAND[8]
    # },
    # {
    #     'marketpalce': 'ozon',
    #     'brand': NAME_BRAND[3]
    # },

]

BRANDS_BY_DIRECTION = {
    "Завод бытовой химии": [NAME_BRAND[15], NAME_BRAND[16], NAME_BRAND[17], NAME_BRAND[18]],
    # "Завод бытовой химии": [NAME_BRAND[10], NAME_BRAND[12]],
    # "Швейное производство": [NAME_BRAND[7]],
    "Фабрика деревянных изделий": [NAME_BRAND[13], NAME_BRAND[14]],
    # "Фабрика деревянных изделий": [NAME_BRAND[6]],
    # "Продукты питания": [NAME_BRAND[3], NAME_BRAND[4], NAME_BRAND[0]],
    # "УстьеЛес Групп": [NAME_BRAND[11]],
}

ACCESS = {
    '1422194909': [x for _, x in NAME_BRAND.items()],
    '424814919': [x for _, x in NAME_BRAND.items()],  # SEO Denis
    '1635185381': [x for _, x in NAME_BRAND.items()],  # Evgeny_Karmansky

    # '848910101': [NAME_BRAND[7]],  # https://t.me/mashashchepelina
    # '904730678': [NAME_BRAND[10]],  # @hellomynameisfabulousss
    # '772342377': [NAME_BRAND[11]],  # Евгений прислал
    # '461274940': [NAME_BRAND[3], NAME_BRAND[4], NAME_BRAND[0]],  # https://t.me/Alesya_C
    # '825951936': [NAME_BRAND[6]],  # https://t.me/KapiJuli
    # '1156080458': [NAME_BRAND[6]],  # https://t.me/AntonPanev
}

ADMIN = ['1422194909', '424814919', '1635185381', '461274940']

SEND_STATISTIC = ['1422194909', '424814919', '1635185381', '461274940', '825951936', '1156080458', '904730678', '772342377']
# SEND_STATISTIC = ['1422194909']

# WEEK STATISTIC FROM GOOGLE SHEET
SOURCE_SHEETS = [
    # {
    #     'sheets': '1oo-oMI1R7FCR9TFs4ikRK8otD2vjeSHJVg3GoZ8VRx0',
    #     'brand': NAME_BRAND[3],  # Гринформула ИП Баушев
    #     'week_profit_tab': 'Еженедельные (фактические)',
    #     'market_place': 'wb'
    # },
    # {
    #     'sheets': '1ZbOEh0shN95e5SgB4PGjpxuy5uTbkNeh2LweeUz_Ee8',
    #     'brand': NAME_BRAND[7],  # Щепелина Little Dreams
    #     'week_profit_tab': 'Еженедельные (фактические)',
    #     'market_place': 'wb'
    # },
    # {
    #     'sheets': '1bbujoJz3pPNYkZnPSOq6rIy97Lnu28kVR5_7AW7OhIg',
    #     'brand': NAME_BRAND[6],  # ФДИ - Kronly - ФАБРИКА ДЕРЕВЯННЫХ ИЗДЕЛИЙ
    #     'week_profit_tab': 'Еженедельные (фактические)',
    #     'market_place': 'wb'
    # }
]

MAX_ROWS = 10000

API_KEY_GOOGLE = os.getenv('API_KEY_GOOGLE')
