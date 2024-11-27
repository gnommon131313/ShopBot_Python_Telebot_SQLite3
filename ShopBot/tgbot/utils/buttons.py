from telebot import types
from tgbot.utils import filters, sql_facade
import sqlite3


def info(text: str) -> types.InlineKeyboardButton:
    return types.InlineKeyboardButton(text=text, callback_data='pass')

def chapter(value: str, page: int) -> types.InlineKeyboardButton:
    emoji = "📖" if value == 'catalog' else "🗑️" if value == 'basket' else "🏷️"

    return types.InlineKeyboardButton(
        text=emoji + value,
        callback_data=filters.chapter_load.new(chapter=value, page=page))

def products(products_pool: list, page: int, page_capacity: int) -> list:
    start = page * page_capacity
    end = start + page_capacity
    products_to_load = products_pool[start:end]
    products_btn = []

    for product in products_to_load:
        products_btn.append(types.InlineKeyboardButton(
            text=f"{product[1]}",
            callback_data=filters.product_card_load.new(id=product[0])))

    return products_btn

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

def basket_staff(product_id: int, user_id: int) -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup()
    product_in_basket = sql_facade.execute([['SELECT * FROM basket_products WHERE product_id = ?', (product_id,)]])

    if product_in_basket:
        change_quantity_1 = types.InlineKeyboardButton(
            text="-5",
            callback_data=filters.db_update.new(
                table='basket_products', parameters=f"-5, {product_id}"))
        change_quantity_2 = types.InlineKeyboardButton(
            text="-1",
            callback_data=filters.db_update.new(
                table='basket_products', parameters=f"-1, {product_id}"))
        change_quantity_3 = types.InlineKeyboardButton(
            text="+5",
            callback_data=filters.db_update.new(
                table='basket_products', parameters=f"5, {product_id}"))
        change_quantity_4 = types.InlineKeyboardButton(
            text="+1",
            callback_data=filters.db_update.new(
                table='basket_products', parameters=f"1, {product_id}"))
        quantity = info(f"{product_in_basket[3]}")

        keyboard.row(
            change_quantity_1,
            change_quantity_2,
            quantity,
            change_quantity_3,
            change_quantity_4)

    if product_in_basket:
        toggle = types.InlineKeyboardButton(
            text="❌🗑️remove from basket",
            callback_data=filters.db_delete.new(
                table='basket_products', parameters=f"{product_id}"))
    else:
        toggle = types.InlineKeyboardButton(
            text="💚🗑️add to basket",
            callback_data=filters.db_insert.new(
                table='basket_products', parameters=f"{product_id}, {user_id}, 1"))
    keyboard.row(toggle)

    return keyboard