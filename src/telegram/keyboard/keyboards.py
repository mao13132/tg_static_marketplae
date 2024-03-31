from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, \
    InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


class Admin_keyb:
    def start_keyb(self, current_time):
        self._start_key = InlineKeyboardMarkup(row_width=1)

        self._start_key.add(InlineKeyboardButton(text=f'📊 Получить статистику', callback_data='get_statistic'))

        self._start_key.add(InlineKeyboardButton(
            text=f'⏱ Изменить время ({current_time})', callback_data='change_time'))

        return self._start_key

    def back(self):
        self._start_key = InlineKeyboardMarkup(row_width=1)

        self._start_key.add(InlineKeyboardButton(text=f'🔙 Назад', callback_data='back'))

        return self._start_key
