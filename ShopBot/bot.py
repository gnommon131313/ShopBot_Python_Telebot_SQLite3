from tgbot.handlers import admin, app, user
from tgbot.utils import filters, states, database_builder
from tgbot import config
from telebot import TeleBot
from telebot.storage import StateMemoryStorage


state_storage = StateMemoryStorage()  # ! В реальном проекте заменить на redis, ...
bot = TeleBot(config.TOKEN, state_storage=state_storage, num_threads=5)

def register_handlers():
    app_ = app.App()
    user_ = user.User()

    def database_handler() -> None:
        bot.register_callback_query_handler(
            app_.basket_db.update, func=None, callback_config=filters.basket_db_update.filter(), pass_bot=True)

    def admin_handler() -> None:
        bot.register_message_handler(admin.some_start, commands=['debug'], admin=True, pass_bot=True)

    def app_handler() -> None:
        bot.register_message_handler(app_.menu_load, commands=['start'], pass_bot=True)
        bot.register_callback_query_handler(app_.menu_load_adapter, func=lambda call: call.data == 'menu_load', pass_bot=True)
        bot.register_callback_query_handler(
            app_.chapter_load, func=None, callback_config=filters.chapter_load.filter(), pass_bot=True)
        bot.register_callback_query_handler(
            app_.product_card_load, func=None, callback_config=filters.product_card_load.filter(), pass_bot=True)
        bot.register_callback_query_handler(app_.make_an_order, func=lambda call: call.data == 'make_an_order', pass_bot=True)

    def user_handler() -> None:
        bot.register_message_handler(user_.cancel, commands=['cancel'], admin=False, pass_bot=True)
        bot.register_message_handler(user_.make_an_order, commands=['order'], admin=False, pass_bot=True)
        bot.register_message_handler(
            user_.get_name,
            func=lambda message: bot.get_state(message.from_user.id) == states.User.get_name.name,
            admin=False, pass_bot=True)
        bot.register_message_handler(
            user_.get_phone,
            func=lambda message: bot.get_state(message.from_user.id) == states.User.get_phone.name,
            admin=False, pass_bot=True)
        bot.register_message_handler(
            user_.get_address,
            func=lambda message: bot.get_state(message.from_user.id) == states.User.get_address.name,
            admin=False, pass_bot=True)

    database_handler()
    admin_handler()
    app_handler()
    user_handler()

register_handlers()
database_builder.build()
filters.bind(bot)
bot.infinity_polling()