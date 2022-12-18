from aiogram import Bot, types, Dispatcher
import sqlite3
from data import config
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)

connect = sqlite3.connect('data_base/base.db')
cursor = connect.cursor()

dp = Dispatcher(bot, storage=MemoryStorage())
