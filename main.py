from aiogram.utils import executor
from create_bot import dp
from handlers import user, admin
from database import order_database


async def on_startup(_):
    order_database.sql_start()
    print("in online")

admin.register_handlers_admin(dp)
user.register_handlers_user(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
