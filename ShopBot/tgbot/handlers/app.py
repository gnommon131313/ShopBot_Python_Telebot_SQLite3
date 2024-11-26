from telebot import TeleBot
from telebot import types
from tgbot.utils import filters
from tgbot.database import goods_db , basket_db, order_db
import math
from tgbot.utils import  buttons
from tgbot import config
import sqlite3

class App:
    def __init__(self) -> None:
        self.__basket_db = basket_db.Database()
        self.__order_db = order_db.Database()
        self.__keyboard = types.InlineKeyboardMarkup()
        self.__chapter = ''
        self.__page = 0
        self.__page_capacity = 5

    @property
    def basket_db(self):
        return self.__basket_db

    def menu_load(self, message: types.Message, bot: TeleBot) -> None:
        def create_keyboard() -> None:
            self.__keyboard = types.InlineKeyboardMarkup()
            self.__keyboard.row(
                buttons.chapter('catalog',0),
                buttons.chapter('basket',0),
                buttons.chapter('order',0))

        def edit_message() -> None:
            if message.text:
                if "/" in message.text:
                    bot.send_message(message.chat.id, text="menu:", reply_markup=self.__keyboard)
                else:
                    # Команды нельзя отредактировать (+бот может редактировать только свои собственные сообщения)
                    bot.edit_message_text(text="menu:", chat_id=message.chat.id, message_id=message.message_id,
                                      reply_markup=self.__keyboard)
            elif message.photo:
                bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
                bot.send_message(message.chat.id, text="menu:", reply_markup=self.__keyboard)

        create_keyboard()
        edit_message()

    def menu_load_adapter(self, call: types.CallbackQuery, bot: TeleBot) -> None:
        self.menu_load(message=call.message, bot=bot)

    def chapter_load(self, call: types.CallbackQuery, bot: TeleBot) -> None:
        callback_data: dict = filters.chapter_load.parse(callback_data=call.data)
        self.__chapter = callback_data['chapter']
        self.__page = int(callback_data['page'])

        def create_keyboard() -> None:
            goods_storage = None

            if self.__chapter == 'catalog':
                goods_storage = goods_db.goods
            elif self.__chapter == 'basket':
                goods_storage = self.__basket_db.goods
            elif self.__chapter == 'order':
                goods_storage = self.__order_db.order

            page_max = math.floor(len(goods_storage) / self.__page_capacity)

            self.__keyboard = types.InlineKeyboardMarkup()
            self.__keyboard.row(*buttons.goods(goods_storage, self.__page, self.__page_capacity))
            self.__keyboard.row(
                buttons.page_switcher(self.__chapter, self.__page, page_max, -1),
                buttons.info(callback_data['page']),
                buttons.page_switcher(self.__chapter, self.__page, page_max, +1))

            if self.__chapter == 'basket':
                if len(goods_storage) > 0:
                    self.__keyboard.row(buttons.make_an_order())

            self.__keyboard.row(buttons.menu())

        def edit_message() -> None:
            if call.message.text:
                bot.edit_message_text(text=f"{callback_data['chapter']}:", chat_id=call.message.chat.id,
                                      message_id=call.message.id)
                bot.edit_message_reply_markup(call.message.chat.id, call.message.id, reply_markup=self.__keyboard)

            elif call.message.photo:
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                bot.send_message(call.message.chat.id, text=f"{callback_data['chapter']}:", reply_markup=self.__keyboard)

        create_keyboard()
        edit_message()

    def product_card_load(self, call: types.CallbackQuery, bot: TeleBot) -> None:
        callback_data: dict = filters.product_card_load.parse(callback_data=call.data)
        product = next((element for element in goods_db.goods if callback_data['id'] == element['id']), None)

        def create_keyboard() -> None:
            self.__keyboard = buttons.basket_staff(product_id=product['id'], basket_db_goods=self.__basket_db.goods)
            self.__keyboard.row(buttons.chapter(self.__chapter, self.__page))

        def edit_message() -> None:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

            with open(product['image_path'], 'rb') as photo:
                bot.send_photo(chat_id=call.message.chat.id, photo=photo,
                    caption=f"{product['name']}  =  {product['price']}$",
                    reply_markup=self.__keyboard)

        create_keyboard()
        edit_message()

    def make_an_order(self, call: types.CallbackQuery, bot: TeleBot) -> None:
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(
            chat_id=call.message.chat.id,
            text="/order - чтобы оформить заказ")