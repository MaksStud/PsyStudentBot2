from aiogram import types, Dispatcher
import user_message_text
import time
from create_bot import bot
from keyboards import user_kb
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from database import order_database
import random

big_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
small_letters = 'abcdefghijklmnopqrstuvwxyz'
number = '1234567890'
characters = big_letters + small_letters + number


async def id_generation():
    id_list = await order_database.sql_reading_id()
    while True:
        random_number = ''.join(random.choice(characters) for _ in range(15))  # Генеруємо ID з 10 символів
        if random_number not in id_list:
            break
    return random_number


async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, user_message_text.warning_message)
    time.sleep(0.5)
    await bot.send_message(message.from_user.id, user_message_text.start_message, reply_markup=user_kb.kb_start)


async def help_command(message: types.Message):
    await bot.send_message(message.from_user.id, user_message_text.warning_message)
    await bot.send_message(message.from_user.id, user_message_text.help_message, reply_markup=user_kb.kb_execution_time)


async def execution_time_command(message: types.Message):
    await bot.send_message(message.from_user.id, user_message_text.execution_time_message,
                           reply_markup=user_kb.kb_main_menu_return)


async def main_menu(message: types.Message):
    await bot.send_message(message.from_user.id, user_message_text.main_menu_message, reply_markup=user_kb.kb_start)


async def set_offers(message: types.Message):
    await bot.send_message(message.from_user.id, user_message_text.set_offers_message, reply_markup=user_kb.kb_order)
    pass


class Order(StatesGroup):
    order_name = State()
    photo = State()
    description = State()
    email = State()
    order_id = State()


# Початок роботи

async def cm_start(message: types.Message):
    await Order.order_name.set()
    await message.reply('Введіть назву замовлення✏️', reply_markup=user_kb.kb_order_selection)


async def load_order_name(message: types.Message, state: FSMContext):
    async with state.proxy() as date:
        date['order_name'] = message.text
        await Order.next()
        await message.reply('Надішліть одне фото🖼️ що стосується завдання',
                            reply_markup=user_kb.kb_no_phono)


async def load_photo(message: types.Message, state: FSMContext):
    if message.text == 'Без фото🖼️':
        async with state.proxy() as date:
            date['photo'] = 'Без фото'
        await Order.next()
        await message.reply('Введіть тему та опис завдання📖', reply_markup=user_kb.kb_сancel_the_order_submission)
    else:
        async with state.proxy() as date:
            date['photo'] = message.photo[0].file_id
        await Order.next()
        await message.reply('Введіть тему та опис завдання📖', reply_markup=user_kb.kb_сancel_the_order_submission)


async def load_description(message: types.Message, state: FSMContext):
    async with state.proxy() as date:
        date['description'] = message.text
        await Order.next()
        await message.reply('Введіть свій email📧')


async def load_email(message: types.Message, state: FSMContext):
    async with state.proxy() as date:
        date['email'] = message.text
        date['order_id'] = await id_generation()

        await order_database.sql_add_command(date['order_id'], date['order_name'], date['photo'],
                                             date['description'], date['email'])
        await state.finish()
        if date['photo'] != 'Без фото':
            await bot.send_photo(message.from_user.id, date['photo'],
                   f'Замовлення отримане успішно\n\nКод для оплати замолення: {date["order_id"]}\n\nНазва завдання:\n   {date["order_name"]}\n\nТема та опис:\n   {date["description"]}\n\nЕлектрона пошта:\n   {date["email"]}')
        else:
            await bot.send_message(message.from_user.id,
                   f'Замовлення отримане успішно\n\nКод для оплати замолення: {date["order_id"]}\n\nНазва завдання:\n   {date["order_name"]}\n\nТема та опис:\n   {date["description"]}\n\nЕлектрона пошта:\n   {date["email"]}')
        await bot.send_message(message.from_user.id, "Код для оплати втавіть в рядок пункт призначення.", reply_markup=user_kb.kb_order)


async def cancellation(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("Замолення скасоване❌")
    await bot.send_message(message.from_user.id, user_message_text.set_offers_message, reply_markup=user_kb.kb_order)


async def delete_other_message(message: types.Message):
    print("other message -> " + "text = " + str(message.text) + " | " + "id = " + str(
        message.message_id) + " | " + "date = "
          + str(message.date) + " | name =  " + str(message.from_user.last_name) + " " + (
              message.from_user.first_name) + " | user name =  " + str(message.from_user.username))
    print()
    await message.delete()


def register_handlers_user(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'restart'])
    dp.register_message_handler(help_command, lambda message: message.text == 'Допомога❓')
    dp.register_message_handler(set_offers, lambda message: message.text == 'Список пропозицій📄')
    dp.register_message_handler(main_menu, lambda message: message.text == 'Головна сторінка↩️')
    dp.register_message_handler(execution_time_command, lambda message: message.text == 'Час виконання⏳')
    dp.register_message_handler(cm_start, lambda message: message.text == 'Замовити📝', state=None, )
    dp.register_message_handler(cancellation, Text(equals='Скасувати подачу замовлення❌', ignore_case=True), state="*")
    dp.register_message_handler(load_order_name, state=Order.order_name)
    dp.register_message_handler(load_photo, content_types=['photo', 'text'], state=Order.photo)
    dp.register_message_handler(load_description, state=Order.description)
    dp.register_message_handler(load_email, state=Order.email)
