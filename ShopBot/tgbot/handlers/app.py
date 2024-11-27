from telebot import TeleBot
from telebot import types
from tgbot.utils import filters, sql_facade
import math
from tgbot.utils import  buttons


class App:
    def __init__(self) -> None:
        self.__keyboard = types.InlineKeyboardMarkup()
        self.__chapter = ''
        self.__page = 0
        self.__page_capacity = 5

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
        products = []

        if self.__chapter == 'catalog':
            products = sql_facade.execute([['SELECT * FROM products', ()]], 'all')

        elif self.__chapter == 'basket':
            products = sql_facade.execute(
            [['''
                SELECT products.* 
                FROM basket_products
                INNER JOIN products ON basket_products.product_id = products.id
                ORDER BY id ASC
            ''', ()]],
            'all')

        elif self.__chapter == 'order':
            # Показывает не заказы, а все продукты во всех заказах
            products = sql_facade.execute(
            [['''
                SELECT products.* 
                FROM order_products
                INNER JOIN products ON order_products.product_id = products.id
                WHERE order_products.user_id = ?
                ORDER BY id ASC
            ''', (call.from_user.id,)]],
            'all')

        def create_keyboard() -> None:
            page_max = math.floor(len(products) / self.__page_capacity)

            self.__keyboard = types.InlineKeyboardMarkup()
            self.__keyboard.row(*buttons.products(products, self.__page, self.__page_capacity))
            self.__keyboard.row(
                buttons.page_switcher(self.__chapter, self.__page, page_max, -1),
                buttons.info(callback_data['page']),
                buttons.page_switcher(self.__chapter, self.__page, page_max, +1))

            if self.__chapter == 'basket':
                if len(products) > 0:
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
        product = sql_facade.execute([['SELECT * FROM products WHERE id = ?', (callback_data['id'],)]])

        def create_keyboard() -> None:
            self.__keyboard = buttons.basket_staff(product_id=product[0], user_id=call.from_user.id)
            self.__keyboard.row(buttons.chapter(self.__chapter, self.__page))

        def edit_message() -> None:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

            with open(product[4], 'rb') as photo:
                bot.send_photo(chat_id=call.message.chat.id, photo=photo,
                    caption=f"{product[1]}  =  {product[3]}$",
                    reply_markup=self.__keyboard)

        create_keyboard()
        edit_message()