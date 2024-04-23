import sqlite3 as sq
from create_bot import bot


def sql_start():
    global base, cur
    base = sq.connect('order.db')
    cur = base.cursor()
    if base:
        print('The database is connected')
    base.execute('CREATE TABLE IF NOT EXISTS task_list(order_id TEXT PRIMARE KEY, order_name TEXT, photo TEXT, description TEXT, email TEXT)')
    base.commit()


async def sql_add_command(order_id, order_name, photo, description, email):
    cur.execute('INSERT INTO task_list VALUES (?, ?, ?, ?, ?)', (order_id, order_name, photo, description, email))
    base.commit()
    print("Успішно додано")


def isEmpty_data_base():
    cur.execute("SELECT EXISTS (SELECT 1 FROM task_list LIMIT 1)")
    result = cur.fetchone()
    return not result[0]


async def sql_data_uploading(message):
    if not isEmpty_data_base():
        for ret in cur.execute('SELECT * FROM task_list').fetchall():
            if ret[2] == 'Без фото':
                await bot.send_message(message.from_user.id,
                                     f'ID Замолення: {ret[0]}\n\nНазва завдання: {ret[1]}\n\nТема та опис: {ret[3]}\n\nЕлектрона пошта: {ret[4]}')
            elif ret[2] != 'Без фото':
                await bot.send_photo(message.from_user.id, ret[2],
                                     f'ID Замолення: {ret[0]}\n\nНазва завдання: {ret[1]}\n\nТема та опис: {ret[3]}\n\nЕлектрона пошта: {ret[4]}')
            else:
                print('Error')
    elif isEmpty_data_base():
        await bot.send_message(message.from_user.id, "Немає замовлень")


async def sql_reading_id():
    id_list = []
    for ret in cur.execute('SELECT * FROM task_list').fetchall():
        id_list.append(ret[0])
    return id_list


# Функція, яка видаляє рядок з бази даних за ID
def delete_order(order_id):
    # Видалити рядок з таблиці task_list за ID
    cur.execute("DELETE FROM task_list WHERE order_id = ?", (order_id,))
    base.commit()




