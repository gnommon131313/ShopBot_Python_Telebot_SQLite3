from tgbot import config
from telebot import TeleBot, types
from tgbot.utils import filters
from tgbot.database import goods_db as goods_db
import copy
from tgbot.utils import buttons
import numpy as np


class Database:
    def __init__(self) -> None:
        self.__goods = [{'id': '2', 'name': '2 товар', 'description': 'лучший в мире товар', 'price': '222', 'quantity': '2', 'image_path': f'{config.GOODS_IMAGE_PATH}EggRaw.png'},
            {'id': '9', 'name': '9 товар', 'description': 'лучший в мире товар', 'price': '999', 'quantity': '9', 'image_path': f'{config.GOODS_IMAGE_PATH}Meat.png'},
            {'id': '12', 'name': '12 товар', 'description': 'лучший в мире товар', 'price': '1222', 'quantity': '12', 'image_path': f'{config.GOODS_IMAGE_PATH}PlateWood.png'},]

    @property
    def goods(self) -> list:
        return self.__goods

    def update(self, call: types.CallbackQuery, bot: TeleBot) -> None:
        callback_data: dict = filters.basket_db_update.parse(callback_data=call.data)
        product = next((element for element in goods_db.goods if callback_data['id'] == element['id']), None)
        product_in_basket = next((element for element in self.__goods if product['id'] == element['id']), None)

        if callback_data['toggle'] == 'add':
            if product_in_basket:
                return

            product_copy = copy.deepcopy(product)
            product_copy['quantity'] = 1
            self.__goods.append(product_copy)
            self.__goods = sorted(self.__goods, key=lambda element: int(element['id']))

        elif callback_data['toggle'] == 'remove':
            if product_in_basket:
                self.__goods.remove(product_in_basket)

        else:
            if not product_in_basket:
                return

            new_quantity = int(product_in_basket['quantity']) + int(callback_data['quantity'])
            new_quantity = np.clip(new_quantity, 1, 20)
            product_in_basket['quantity'] = str(new_quantity)

        def edit_message() -> None:
            keyboard = buttons.basket_staff(product_id=product['id'], basket_db_goods=self.__goods)
            keyboard.row(buttons.menu())
            bot.edit_message_reply_markup(call.message.chat.id, call.message.id, reply_markup=keyboard)

        edit_message()