import os

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), 'src', '.env'))

ADMIN = ['1422194909']

TOKEN = os.getenv('TOKEN')

START_MESSAGE = 'Стартовое сообщение'

OZON_API_KEY_LIST = {
    'Benerich': [os.getenv('CLIENT_ID1'), os.getenv('API_KEY1')],
    'CaptainOil': [os.getenv('CLIENT_ID2'), os.getenv('API_KEY2')],
    'ErgonomOffice': [os.getenv('CLIENT_ID3'), os.getenv('API_KEY3')],
    'greenformula': [os.getenv('CLIENT_ID4'), os.getenv('API_KEY4')],
    'Guru': [os.getenv('CLIENT_ID5'), os.getenv('API_KEY5')],
    'iGGi': [os.getenv('CLIENT_ID6'), os.getenv('API_KEY6')],
    'Kronly': [os.getenv('CLIENT_ID7'), os.getenv('API_KEY7')],
    'Little Dreams': [os.getenv('CLIENT_ID8'), os.getenv('API_KEY8')],
    'Militon': [os.getenv('CLIENT_ID9'), os.getenv('API_KEY9')],
    'Udnet': [os.getenv('CLIENT_ID10'), os.getenv('API_KEY10')],
}
