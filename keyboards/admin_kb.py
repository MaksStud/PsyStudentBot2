from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from keyboards.user_kb import main_menu_button

received_tasks = KeyboardButton('Отримані завдання')
delete_task = KeyboardButton('Видалити завдання')

kb_for_data = ReplyKeyboardMarkup(resize_keyboard=True).add(received_tasks).insert(delete_task).add(main_menu_button)