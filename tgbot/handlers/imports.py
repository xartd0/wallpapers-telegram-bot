from tgbot import db
from tgbot.config import load_config
from aiogram import Dispatcher, Bot
from datetime import datetime

config = load_config(".env")
bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
db = db.Data("tgbot/database/database.db")
now = datetime.now()