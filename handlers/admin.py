from aiogram import types, Dispatcher
from create_bot import bot
from keyboards import admin_kb
from database import order_database
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


def is_admin(user_id):
    admins_list = [890407600, 2070415763]
    return user_id in admins_list


async def login_to_admin(message: types.Message):
    if is_admin(message.from_user.id):
        await bot.send_message(message.from_user.id, "Вітаю в адмінці", reply_markup=admin_kb.kb_for_data)
    else:
        await bot.send_message(message.from_user.id, "Дія не доступна")


async def received_tasks(message: types.Message):
    if is_admin(message.from_user.id):
        await order_database.sql_data_uploading(message)
    else:
        await bot.send_message(message.from_user.id, "Дія не доступна")


class Delete_order_state(StatesGroup):
    order_id = State()


async def cm_start(message: types.Message):
    await Delete_order_state.order_id.set()
    await message.reply("Введіть id замоленя")


async def delete_order(message: types.Message, state: FSMContext):
    async with state.proxy() as date:
        date["id"] = message.text
    order_database.delete_order(date["id"])
    await message.reply("Видалено", reply_markup=admin_kb.kb_for_data)
    await state.finish()


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(login_to_admin, commands=['admin'])
    dp.register_message_handler(login_to_admin, lambda message: message.text == 'mZaaH7J6IxvTdzhZgykx')
    dp.register_message_handler(received_tasks, lambda message: message.text == 'Отримані завдання')
    dp.register_message_handler(cm_start, lambda message: message.text == 'Видалити завдання', state=None, )
    dp.register_message_handler(delete_order, state=Delete_order_state.order_id)
