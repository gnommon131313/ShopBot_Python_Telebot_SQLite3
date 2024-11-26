from telebot import TeleBot
from telebot import types
from tgbot.utils import states
from tgbot import config
import sqlite3


class User:
    def __init__(self) -> None:
       pass

    def cancel(self, message: types.Message, bot: TeleBot):
        bot.delete_state(message.from_user.id, message.chat.id)
        bot.send_message(message.chat.id, text="Ваша информация была очищена")
        bot.send_message(message.chat.id, text="/start чтобы начать")

    def make_an_order(self, message: types.Message, bot: TeleBot) -> None:
        try:
            # Проверить есть ли товары в корзине
            pass
        except ValueError:
            bot.send_message(chat_id=message.chat.id, text="Error")
            return

        def work_with_db() -> None:
            conn = sqlite3.connect(config.DATABASE)
            cursor = conn.cursor()
            cursor.execute('INSERT OR IGNORE INTO users (id) VALUES (?)', (message.from_user.id,))
            conn.commit()
            conn.close()

        work_with_db()

        bot.set_state(message.from_user.id, states.User.get_name, message.chat.id)
        bot.send_message(chat_id=message.chat.id, text="Введите свои данные: \n/cancel - чтобы отменить")
        bot.send_message(chat_id=message.chat.id, text="Укажите Имя")

    def get_name(self, message: types.Message, bot: TeleBot):
        try:
            # Валидация
            pass
        except ValueError:
            bot.send_message(message.chat.id, text="Укажите корректное имя")
            return

        def work_with_db() -> None:
            conn = sqlite3.connect(config.DATABASE)
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET name = ? WHERE id = ?", (message.text, message.from_user.id))
            conn.commit()
            conn.close()

        work_with_db()

        bot.set_state(message.from_user.id, states.User.get_phone, message.chat.id)
        bot.send_message(message.chat.id, text="Укажите номер телефона")

    def get_phone(self, message: types.Message, bot: TeleBot):
        try:
            # Валидация
            pass
        except ValueError:
            bot.send_message(message.chat.id, text="Укажите корректный номер телефона")
            return

        def work_with_db() -> None:
            conn = sqlite3.connect(config.DATABASE)
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET phone = ? WHERE id = ?", (message.text, message.from_user.id))
            conn.commit()
            conn.close()

        work_with_db()

        bot.set_state(message.from_user.id, states.User.get_address, message.chat.id)
        bot.send_message(message.chat.id, text="Укажите адрес")

    def get_address(self, message: types.Message, bot: TeleBot):
        try:
            # Валидация
            pass
        except ValueError:
            bot.send_message(message.chat.id, text="Укажите корректный адрес")
            return

        def order_placed() -> None:
            print("заказ помещен в базу под id пользователя")

            def work_with_db() -> None:
                conn = sqlite3.connect(config.DATABASE)
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE users SET address = ? WHERE id = ?", (message.text, message.from_user.id))
                # Удалить из базы корзины
                # Поместить в базу заказов
                conn.commit()
                conn.close()

            work_with_db()
        order_placed()

        bot.send_message(chat_id=message.chat.id, text="Заказ успешно оформлен!")
        bot.send_message(chat_id=message.chat.id, text="Посмотреть свои заказы: 'Menu-Order'")