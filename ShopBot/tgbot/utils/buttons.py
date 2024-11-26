from telebot import types
from tgbot.utils import filters


def info(text: str) -> types.InlineKeyboardButton:
    return types.InlineKeyboardButton(
        text=text,
        callback_data='pass')

def chapter(value: str, page: int) -> types.InlineKeyboardButton:
    emoji = "📖" if value == 'catalog' else "🗑️" if value == 'basket' else "🏷️"

    return types.InlineKeyboardButton(
        text=emoji + value,
        callback_data=filters.chapter_load.new(chapter=value, page=page))

def goods(database: list, page: int, page_capacity: int) -> list:
    start = page * page_capacity
    end = start + page_capacity
    goods_to_load = database[start:end]
    goods_btn = []

    for product in goods_to_load:
        goods_btn.append(types.InlineKeyboardButton(
            text=f"{product['name']}",
            callback_data=filters.product_card_load.new(id=product['id'])))

    return goods_btn

def page_switcher(chapter: str, page: int, page_max: int, value: int) -> types.InlineKeyboardButton:
    page_new = max(min(page + value, page_max), 0)
    action = "increase" if page_new > page else "decrease" if page_new < page else "pass"
    text = f"{"➡️" if action == "increase" else "⬅️" if action == "decrease" else "-"}"

    return types.InlineKeyboardButton(
        text=text,
        callback_data=filters.chapter_load.new(chapter=chapter, page=f"{page_new}") if action != "pass" else 'pass')

def menu() -> types.InlineKeyboardButton:
    return types.InlineKeyboardButton(
        text="↩️",
        callback_data='menu_load')

def make_an_order() -> types.InlineKeyboardButton:
    return types.InlineKeyboardButton(text=f"📦make an order", callback_data='make_an_order')

def basket_staff(product_id: dict, basket_db_goods) -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup()
    product_in_basket = next((element for element in basket_db_goods if product_id == element['id']), None)

    if product_in_basket:
        change_quantity_1 = types.InlineKeyboardButton(
            text="-5",
            callback_data=filters.basket_db_update.new(
                id=product_in_basket['id'], toggle='', quantity='-5'))
        change_quantity_2 = types.InlineKeyboardButton(
            text="-1",
            callback_data=filters.basket_db_update.new(
                id=product_in_basket['id'], toggle='', quantity='-1'))
        change_quantity_3 = types.InlineKeyboardButton(
            text="+5",
            callback_data=filters.basket_db_update.new(
                id=product_in_basket['id'], toggle='', quantity='5'))
        change_quantity_4 = types.InlineKeyboardButton(
            text="+1",
            callback_data=filters.basket_db_update.new(
                id=product_in_basket['id'], toggle='', quantity='1'))
        quantity = info(f"{product_in_basket['quantity']}")

        keyboard.row(
            change_quantity_1,
            change_quantity_2,
            quantity,
            change_quantity_3,
            change_quantity_4)

    toggle = types.InlineKeyboardButton(
        text=f"{"❌🗑️remove from basket" if product_in_basket else "💚🗑️add to basket"}",
        callback_data=filters.basket_db_update.new(
            id=product_id, toggle='remove' if product_in_basket else 'add', quantity=''))

    keyboard.row(toggle)

    return keyboard