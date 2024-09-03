import logging

import aiohttp

from settings import TOKEN


class Telegram:
    def __init__(self):
        self.TOKEN = TOKEN

        self.ADMIN_TELEGRAM = '1422194909'

        self.ID_CHAT = '1422194909'

        self.session_timeout = aiohttp.ClientTimeout(total=1, connect=.1)

    async def send_message(self, text):
        url_req = "https://api.telegram.org/bot" + self.TOKEN + "/sendMessage" + "?chat_id=" + \
                  self.ADMIN_TELEGRAM + "&text=tg_stat_market" + text

        try:

            async with aiohttp.ClientSession(timeout=self.session_timeout) as session:
                async with session.get(url_req, timeout=aiohttp.ClientTimeout(total=60)) as resul:
                    response = await resul.text()

                    if resul.status != 200:
                        logging.error(f'ошибка при отправке сообщения telegram debugger. Код "{resul.status}"')

                    return response

        except Exception as es:

            logging.warning(f'Ошибка при отправке сообщения в телеграм "{es}"')

            return False
