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
}

OZON_API_KEY_LIST = {
    NAME_BRAND[13]: [os.getenv('CLIENT_ID13'), os.getenv('OZON_API_KEY13')],
    NAME_BRAND[15]: [os.getenv('CLIENT_ID15'), os.getenv('OZON_API_KEY15')],
    NAME_BRAND[16]: [os.getenv('CLIENT_ID16'), os.getenv('OZON_API_KEY16')],
    NAME_BRAND[17]: [os.getenv('CLIENT_ID17'), os.getenv('OZON_API_KEY17')],
    NAME_BRAND[18]: [os.getenv('CLIENT_ID18'), os.getenv('OZON_API_KEY18')],
}

WB_API_KEY_LIST = {
    NAME_BRAND[13]: [os.getenv('api_key13'), os.getenv('api_key13')],
    NAME_BRAND[14]: [os.getenv('api_key14'), os.getenv('api_key14')],
    NAME_BRAND[15]: [os.getenv('api_key15'), os.getenv('api_key15')],
    NAME_BRAND[16]: [os.getenv('api_key16'), os.getenv('api_key16')],
    NAME_BRAND[17]: [os.getenv('api_key17'), os.getenv('api_key17')],
    NAME_BRAND[18]: [os.getenv('api_key18'), os.getenv('api_key18')],
}


STOP_BRAND_FILTER = [
    {
        'marketpalce': 'ozon',
        'brand': NAME_BRAND[14]
    },

    # {
    #     'marketpalce': 'ozon',
    #     'brand': NAME_BRAND[15]
    # },
    # {
    #     'marketpalce': 'wb',
    #     'brand': NAME_BRAND[13]
    # },
    # {
    #     'marketpalce': 'wb',
    #     'brand': NAME_BRAND[14]
    # },
    # {
    #     'marketpalce': 'wb',
    #     'brand': NAME_BRAND[16]
    # },
    # {
    #     'marketpalce': 'wb',
    #     'brand': NAME_BRAND[17]
    # },
    # {
    #     'marketpalce': 'wb',
    #     'brand': NAME_BRAND[16]
    # },
    # {
    #     'marketpalce': 'wb',
    #     'brand': NAME_BRAND[18]
    # },
]

BRANDS_BY_DIRECTION = {
    "Завод бытовой химии": [NAME_BRAND[15], NAME_BRAND[16], NAME_BRAND[17], NAME_BRAND[18], 'biostiq'],
    # "Завод бытовой химии": [NAME_BRAND[10], NAME_BRAND[12]],
    # "Швейное производство": [NAME_BRAND[7]],
    "Фабрика деревянных изделий": [NAME_BRAND[13], NAME_BRAND[14]],
    # "Фабрика деревянных изделий": [NAME_BRAND[6]],
    # "Продукты питания": [NAME_BRAND[3], NAME_BRAND[4], NAME_BRAND[0]],
    # "УстьеЛес Групп": [NAME_BRAND[11]],
}

# Бренды для отдельной статистики (без учета регистра)
# Ключ = бренд который должны иметь товары (lower) - для сопоставления
# Значение = не используется для записи, только для сопоставления
# Если товар имеет такой бренд - он исключается из статистики по API-ключу
# и записывается в статистику под НАЙДЕННЫМ брендом товара (оригинальный регистр)
BRANDS_SEPARATE_STATS = {
    'biostiq': 'biostiq',
}

ACCESS = {
    '1422194909': [x for _, x in NAME_BRAND.items()] + [x for x, _ in BRANDS_SEPARATE_STATS.items()],
    '424814919': [x for _, x in NAME_BRAND.items()] + [x for x, _ in BRANDS_SEPARATE_STATS.items()],  # SEO Denis
    '1635185381': [x for _, x in NAME_BRAND.items()] + [x for x, _ in BRANDS_SEPARATE_STATS.items()],  # Evgeny_Karmansky
    '1156080458': [NAME_BRAND[13], NAME_BRAND[14]],  # https://t.me/AntonPanev

    # '848910101': [NAME_BRAND[7]],  # https://t.me/mashashchepelina
    # '904730678': [NAME_BRAND[10]],  # @hellomynameisfabulousss
    # '772342377': [NAME_BRAND[11]],  # Евгений прислал
    # '461274940': [NAME_BRAND[3], NAME_BRAND[4], NAME_BRAND[0]],  # https://t.me/Alesya_C
    # '825951936': [NAME_BRAND[6]],  # https://t.me/KapiJuli
}

ADMIN = ['1422194909', '424814919', '1635185381', '461274940']

SEND_STATISTIC = ['1422194909', '1156080458', '424814919', '1635185381', '461274940', '825951936', '904730678', '772342377']
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

# Порядок брендов для отображения (меньше число = раньше показывается)
# Если бренд не в списке - он показывается после всех кто есть в списке
BRANDS_ORDER = {
    'Kronly': 1,
    'Kronly Agent': 2,
    'Spets ЗБХ': 3,
    'biostiq': 4,
    'Spets ЗФП': 5,
    'Spets Контракт': 6,
    'Spets Юникорн': 7,
}
