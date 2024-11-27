from telebot import TeleBot
from telebot import types
from tgbot.utils import filters, sql_facade
import numpy
from tgbot.utils import  buttons


def insert(call: types.CallbackQuery, bot: TeleBot) -> None:
    callback_data: dict = filters.db_insert.parse(callback_data=call.data)
    parameters = callback_data['parameters'].split(", ")  # Превратит в список в любом случае

    if callback_data['table'] == 'basket_products':
        sql_facade.execute(
            [[f'INSERT OR IGNORE INTO {callback_data['table']} (product_id, user_id, quantity) VALUES (?, ?, ?)',
            parameters]])

    elif callback_data['table'] == 'xxx':
        pass

    def edit_message() -> None:
        keyboard = buttons.basket_staff(product_id=parameters[0], user_id=call.from_user.id)
        keyboard.row(buttons.menu())
        bot.edit_message_reply_markup(call.message.chat.id, call.message.id, reply_markup=keyboard)

    edit_message()

def delete(call: types.CallbackQuery, bot: TeleBot) -> None:
    callback_data: dict = filters.db_delete.parse(callback_data=call.data)
    parameters = callback_data['parameters'].split(", ")

    if callback_data['table'] == 'basket_products':
        sql_facade.execute(
            [[f'DELETE FROM {callback_data['table']} WHERE product_id = ?',
            parameters]])

    elif callback_data['table'] == 'xxx':
        pass

    def edit_message() -> None:
        keyboard = buttons.basket_staff(product_id=parameters[0], user_id=call.from_user.id)
        keyboard.row(buttons.menu())
        bot.edit_message_reply_markup(call.message.chat.id, call.message.id, reply_markup=keyboard)

    edit_message()

def update(call: types.CallbackQuery, bot: TeleBot) -> None:
    callback_data: dict = filters.db_update.parse(callback_data=call.data)
    parameters = callback_data['parameters'].split(", ")

    if callback_data['table'] == 'basket_products':
        product_data = sql_facade.execute(
            [[f'SELECT * FROM {callback_data['table']} WHERE product_id = ?', parameters[1]]])

        quantity = int(product_data[3])
        addend = int(parameters[0])
        summ = numpy.clip(quantity + addend, 1, 10)

        if  quantity == summ:  # Защита от исключения
            return

        parameters[0] = str(summ)

        sql_facade.execute(
            [[f'UPDATE {callback_data['table']} SET quantity = ? WHERE product_id = ?',
            parameters]])

    elif callback_data['table'] == 'xxx':
        pass

    def edit_message() -> None:
        keyboard = buttons.basket_staff(product_id=parameters[1], user_id=call.from_user.id)
        keyboard.row(buttons.menu())
        bot.edit_message_reply_markup(call.message.chat.id, call.message.id, reply_markup=keyboard)

    edit_message()