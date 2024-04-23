from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

offers_button = KeyboardButton('Список пропозицій📄')
help_button = KeyboardButton('Допомога❓')
main_menu_button = KeyboardButton('Головна сторінка↩️')
execution_time = KeyboardButton('Час виконання⏳')

kb_start = ReplyKeyboardMarkup(resize_keyboard=True)

kb_start.add(offers_button).insert(help_button)

kb_main_menu_return = ReplyKeyboardMarkup(resize_keyboard=True)

kb_main_menu_return.insert(main_menu_button)

kb_execution_time = ReplyKeyboardMarkup(resize_keyboard=True).add(execution_time)

presentation = KeyboardButton("Презентація стандарт📃")
extended_presentation = KeyboardButton("Презентація розширена📜")
practical = KeyboardButton("Практичні стандарт🖋️")
сreative_works = KeyboardButton("Творчі звавдання💭")
course_work_2 = KeyboardButton("Курсова робота(2 курс)📒")
course_work_3 = KeyboardButton("Курсова робота(3 курс)📕")

kb_order_selection = ReplyKeyboardMarkup(resize_keyboard=True).add(presentation).add(extended_presentation).add(practical).add(сreative_works).add(course_work_2).add(course_work_3).add(main_menu_button)

order = KeyboardButton("Замовити📝")

kb_order = ReplyKeyboardMarkup(resize_keyboard=True).add(order).add(main_menu_button)

no_photo = KeyboardButton('Без фото🖼️')
сancel_the_order_submission = KeyboardButton('Скасувати подачу замовлення❌')

kb_no_phono = ReplyKeyboardMarkup(resize_keyboard=True).add(no_photo).add(сancel_the_order_submission)
kb_сancel_the_order_submission = ReplyKeyboardMarkup(resize_keyboard=True).add(сancel_the_order_submission)