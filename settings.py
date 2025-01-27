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
    3: 'GreenFormula',
    4: 'Guru',
    0: 'Benerich',
    7: 'Little Dreams',
    8: 'Militon',
    6: 'Kronly',  # это ФДИ
    10: 'Spets',
}

STOP_BRAND_FILTER = [
    {
        'marketpalce': 'wb',
        'brand': NAME_BRAND[4]
    },
    {
        'marketpalce': 'wb',
        'brand': NAME_BRAND[0]
    },
    {
        'marketpalce': 'wb',
        'brand': NAME_BRAND[8]
    },

]

BRANDS_BY_DIRECTION = {
    "Завод бытовой химии": [NAME_BRAND[10]],
    "Швейное производство": [NAME_BRAND[7]],
    "Фабрика деревянных изделий": [NAME_BRAND[6]],
    "Продукты питания": [NAME_BRAND[3], NAME_BRAND[4], NAME_BRAND[0]],
}

OZON_API_KEY_LIST = {
    NAME_BRAND[0]: [os.getenv('CLIENT_ID1'), os.getenv('OZON_API_KEY1')],
    NAME_BRAND[3]: [os.getenv('CLIENT_ID4'), os.getenv('OZON_API_KEY4')],
    NAME_BRAND[4]: [os.getenv('CLIENT_ID5'), os.getenv('OZON_API_KEY5')],
    NAME_BRAND[6]: [os.getenv('CLIENT_ID7'), os.getenv('OZON_API_KEY7')],
    NAME_BRAND[7]: [os.getenv('CLIENT_ID8'), os.getenv('OZON_API_KEY8')],
    NAME_BRAND[8]: [os.getenv('CLIENT_ID9'), os.getenv('OZON_API_KEY9')],
    NAME_BRAND[10]: [os.getenv('CLIENT_ID10'), os.getenv('OZON_API_KEY10')],
}

WB_API_KEY_LIST = {
    NAME_BRAND[3]: [os.getenv('api_key'), os.getenv('api_key2')],
    NAME_BRAND[6]: [os.getenv('api_key_fdi'), os.getenv('api_key_fdi2')],
    NAME_BRAND[7]: [os.getenv('api_key_shelepina'), os.getenv('api_key_shelepina2')],
    NAME_BRAND[10]: [os.getenv('api_key_spets'), os.getenv('api_key_spets2')],
}

ACCESS = {
    '1422194909': [x for _, x in NAME_BRAND.items()],
    '424814919': [x for _, x in NAME_BRAND.items()],  # SEO Denis
    '1635185381': [x for _, x in NAME_BRAND.items()],  # Evgeny_Karmansky
    '461274940': [NAME_BRAND[3], NAME_BRAND[4], NAME_BRAND[0]],  # https://t.me/Alesya_C
    '825951936': [NAME_BRAND[6]],  # https://t.me/KapiJuli
    '1156080458': [NAME_BRAND[6]],  # https://t.me/AntonPanev
    '848910101': [NAME_BRAND[7]],  # https://t.me/mashashchepelina
    '904730678': [NAME_BRAND[10]],  # @hellomynameisfabulousss
}

ADMIN = ['1422194909', '424814919', '1635185381', '461274940']

SEND_STATISTIC = ['1422194909', '424814919', '1635185381', '461274940', '825951936', '1156080458', '848910101', '904730678']
# SEND_STATISTIC = ['1422194909']

# WEEK STATISTIC FROM GOOGLE SHEET
SOURCE_SHEETS = [
    {
        'sheets': '1oo-oMI1R7FCR9TFs4ikRK8otD2vjeSHJVg3GoZ8VRx0',
        'brand': NAME_BRAND[3],  # Гринформула ИП Баушев
        'week_profit_tab': 'Еженедельные (фактические)',
        'market_place': 'wb'
    },
    {
        'sheets': '1ZbOEh0shN95e5SgB4PGjpxuy5uTbkNeh2LweeUz_Ee8',
        'brand': NAME_BRAND[7],  # Щепелина Little Dreams
        'week_profit_tab': 'Еженедельные (фактические)',
        'market_place': 'wb'
    },
    {
        'sheets': '1bbujoJz3pPNYkZnPSOq6rIy97Lnu28kVR5_7AW7OhIg',
        'brand': NAME_BRAND[6],  # ФДИ - Kronly - ФАБРИКА ДЕРЕВЯННЫХ ИЗДЕЛИЙ
        'week_profit_tab': 'Еженедельные (фактические)',
        'market_place': 'wb'
    }
]

MAX_ROWS = 10000

API_KEY_GOOGLE = os.getenv('API_KEY_GOOGLE')
