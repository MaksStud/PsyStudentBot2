from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import user_message_text
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

bot = Bot(token=user_message_text.API_token, parse_mode="html")
dp = Dispatcher(bot, storage=storage, )
