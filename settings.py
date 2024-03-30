import os

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), 'src', '.env'))

ADMIN = ['1422194909']

TOKEN = os.getenv('TOKEN')

START_MESSAGE = 'Стартовое сообщение'
