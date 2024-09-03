import requests

from settings import TOKEN
from src.logger.logger_no_sync import logger_no_sync


class SendlerOneCreate:
    def __init__(self, driver):
        self.TOKEN = TOKEN
        self.ADMIN_TELEGRAM = '1422194909'
        self.ADMIN_LIST = ['1422194909']
        self.driver = driver

    def save_text(self, text):
        url_req = "https://api.telegram.org/bot" + self.TOKEN + "/sendMessage" + "?chat_id=" + \
                  self.ADMIN_TELEGRAM + "&text=tg_stat_market" + text

        try:
            results = requests.get(url_req)
        except Exception as es:
            msg = f'Ошибка при отправке сообщения в телеграм "{es}"'

            logger_no_sync(msg)

            return False

        return True

    def send_file(self, file, text_):
        file_in = open(file, 'rb')

        open_files = {'document': file_in}

        cap = {'caption': text_}

        url_req = "https://api.telegram.org/bot" + self.TOKEN + "/sendDocument?chat_id=" + self.ADMIN_TELEGRAM

        try:
            response = requests.post(url_req, files=open_files)

        except Exception as es:
            msg = f'Ошибка при отправке сообщения с файлом в телеграм "{es}"'

            logger_no_sync(msg)

            return False

        file_in.close()

        print(f"Отправил файл в телеграм")

        return True
