from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, \
    InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

class Call_admin:

    def admin(self):
        self._admin = CallbackData('adm', 'type', 'number', 'id')

        return self._admin


class Admin_keyb(Call_admin):
    def start_keyb(self):
        self._start_key = InlineKeyboardMarkup(row_width=1)

        self._start_key.add(InlineKeyboardButton(text=f'🔑 Пароли', callback_data='menu_pass'))

        self._start_key.add(InlineKeyboardButton(text=f'🙋‍ Добавить пользователя', callback_data='add_user'))

        self._start_key.add(InlineKeyboardButton(text=f'📧‍ Рассылка', callback_data='sendler'))

        self._start_key.add(InlineKeyboardButton(text=f'🔙 Назад', callback_data='back_start'))

        return self._start_key
