from telebot import TeleBot
from telebot import types
from tgbot.utils import states
from tgbot.utils import sql_facade


class User:
    def __init__(self) -> None:
        self.id = 0

    def cancel(self, message: types.Message, bot: TeleBot):
        bot.delete_state(message.from_user.id, message.chat.id)
        bot.send_message(message.chat.id, text="Ваша информация была очищена")
        bot.send_message(message.chat.id, text="/start чтобы начать")

    def make_an_order(self, call: types.CallbackQuery, bot: TeleBot) -> None:
        self.id = call.from_user.id

        try:
            # Проверить есть ли товары в корзине
            pass
        except ValueError:
            bot.send_message(chat_id=call.message.chat.id, text="Error")
            return

        sql_facade.execute([['INSERT OR IGNORE INTO users (id) VALUES (?)', (self.id,)]])

        bot.set_state(call.from_user.id, states.User.get_name, call.message.chat.id)
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(
            chat_id=call.message.chat.id,
            text="Для оформления заказа введите свои данные: \n/cancel - чтобы отменить")
        bot.send_message(chat_id=call.message.chat.id, text="Укажите Имя")

    def get_name(self, message: types.Message, bot: TeleBot):
        try:
            # Валидация
            pass
        except ValueError:
            bot.send_message(message.chat.id, text="Укажите корректное имя")
            return

        sql_facade.execute([['UPDATE users SET name = ? WHERE id = ?', (message.text, self.id,)]])

        bot.set_state(self.id, states.User.get_phone, message.chat.id)
        bot.send_message(message.chat.id, text="Укажите номер телефона")

    def get_phone(self, message: types.Message, bot: TeleBot):
        try:
            # Валидация
            pass
        except ValueError:
            bot.send_message(message.chat.id, text="Укажите корректный номер телефона")
            return

        sql_facade.execute([['UPDATE users SET phone = ? WHERE id = ?', (message.text, self.id,)]])

        bot.set_state(self.id, states.User.get_address, message.chat.id)
        bot.send_message(message.chat.id, text="Укажите адрес")

    def get_address(self, message: types.Message, bot: TeleBot):
        try:
            # Валидация
            pass
        except ValueError:
            bot.send_message(message.chat.id, text="Укажите корректный адрес")
            return

        bot.send_message(chat_id=message.chat.id, text="Заказ успешно оформлен!")
        bot.send_message(chat_id=message.chat.id, text="Посмотреть свои заказы: menu-order'")

        def order_finished() -> None:
            sql_facade.execute([['UPDATE users SET address = ? WHERE id = ?', (message.text, self.id,)]])

            # Достать из корзины
            user_basket = sql_facade.execute(
                [['SELECT * FROM basket_products WHERE user_id = ?',
                (message.from_user.id,)]], 'all')

            # Удалить из корзины
            sql_facade.execute(
                [['DELETE FROM basket_products WHERE user_id = ?',
                (message.from_user.id,)]])

            # Создать заказ и получить его id
            order_id = sql_facade.execute(
                [[f'INSERT OR IGNORE INTO orders (user_id, order_date) VALUES (?, ?)',
                (message.from_user.id, '2024-11-26')]], 'id')

            print()
            print(type(order_id), order_id)
            print(user_basket)

            # Поместить под заказ
            for row in user_basket:
                sql_facade.execute(
                    [[f'''INSERT OR IGNORE INTO order_products
                     (order_id, product_id, user_id, quantity) VALUES (?, ?, ?, ?)''',
                    (order_id, row[1], message.from_user.id, row[3])]])

            def save_on_json() -> None:
                order = sql_facade.execute(
                    [['SELECT * FROM orders WHERE user_id = ?',
                    (message.from_user.id,)]], 'all')

                print(type(order), order)

            save_on_json()
        order_finished()