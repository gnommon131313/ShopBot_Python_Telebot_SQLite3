import telebot
from telebot import types, SimpleCustomFilter, AdvancedCustomFilter
from telebot.callback_data import CallbackData, CallbackDataFilter
from tgbot import config


chapter_load = CallbackData('chapter', 'page', prefix='prefix_chapter_load')
product_card_load = CallbackData('id', prefix='prefix_product_card_load')
db_insert = CallbackData('table', 'parameters', prefix='prefix_db_insert')
db_delete = CallbackData('table', 'parameters', prefix='prefix_db_delete')
db_update = CallbackData('table', 'parameters', prefix='prefix_db_update')

def bind(bot: telebot.TeleBot):
    bot.add_custom_filter(AdminFilter())
    bot.add_custom_filter(CallbackFilter())


class AdminFilter(SimpleCustomFilter):
    key = 'admin'

    def check(self, message):
        return message.from_user.id in config.ADMIN


class CallbackFilter(AdvancedCustomFilter):
    key = 'callback_config'

    def check(self, call: types.CallbackQuery, callback_filter: CallbackDataFilter):
        return callback_filter.check(query=call)