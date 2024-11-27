import sqlite3
from tgbot import config


def build() -> None:
    conn = sqlite3.connect(config.DATABASE)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        phone TEXT,
        address TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT,
        price REAL NOT NULL,
        image_path TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS basket_products (
        id INTEGER PRIMARY KEY,
        product_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        FOREIGN KEY (product_id) REFERENCES products (id),
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        order_date TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'pending',
        FOREIGN KEY (user_id) REFERENCES user (id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS order_products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders (id),
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (product_id) REFERENCES products (id)
    )
    ''')

    fill_in(cursor)

    conn.commit()
    conn.close()

def fill_in(cursor) -> None:
    def TEST_add_to_basket() -> None:
        pool = [
            (1, 3, 12345, 69),
            (2, 5, 12345, 55),
            (3, 9, 12345, 999)
        ]

        cursor.executemany(
            'INSERT OR IGNORE INTO basket_products (id, product_id, user_id, quantity) VALUES (?, ?, ?, ?)',
            pool)

    def products() -> None:
        image_path = 'tgbot/images/products/'

        pool = [
            (1, "prod 1", "the best of the best", 11, f"{image_path}Egg.png"),
            (2, "prod 2", "the best of the best", 22, f"{image_path}EggRaw.png"),
            (3, "prod 3", "the best of the best", 33, f"{image_path}EggsFried.png"),
            (4, "prod 4", "the best of the best", 44, f"{image_path}Fish.png"),
            (5, "prod 5", "the best of the best", 55, f"{image_path}FishCut.png"),
            (6, "prod 6", "the best of the best", 66, f"{image_path}FishFried.png"),
            (7, "prod 7", "the best of the best", 77, f"{image_path}FishSkeleton.png"),
            (8, "prod 8", "the best of the best", 88, f"{image_path}FriedMeat.png"),
            (9, "prod 9", "the best of the best", 99, f"{image_path}GarbageBag.png"),
            (10, "prod 10", "the best of the best", 100, f"{image_path}Meat.png"),
            (11, "prod 11", "the best of the best", 110, f"{image_path}MeatCut.png"),
            (12, "prod 12", "the best of the best", 120, f"{image_path}PiecesOfMeat.png")
        ]

        cursor.executemany(
            'INSERT OR IGNORE INTO products (id, name, description, price, image_path) VALUES (?, ?, ?, ?, ?)',
            pool)

    # TEST_add_to_basket()
    products()