from tgbot import config
import sqlite3


def execute(args: list, get: str = 'one', database = config.DATABASE):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    for arg in args:
        cursor.execute(arg[0], arg[1])

    result = None

    if get == 'one':
        result = cursor.fetchone()
    elif get == 'all':
        result = cursor.fetchall()

    conn.commit()
    conn.close()

    return result