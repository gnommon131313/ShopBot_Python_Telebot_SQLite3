from tgbot import config
from telebot import TeleBot, types


class Database:
    def __init__(self) -> None:
        self.__order = []

    @property
    def order(self) -> list:
        return self.__order

    def update(self, call: types.CallbackQuery, bot: TeleBot) -> None:
        pass