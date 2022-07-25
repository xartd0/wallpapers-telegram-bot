from aiogram import Dispatcher
from aiogram.types import Message
from tgbot import db
from datetime import datetime
from tgbot.keyboards.inline import *

db = db.Data("tgbot/database/database.db")
now = datetime.now()

async def user_start(message: Message):
    user_id = message.from_user.id
    if db.check_user(user_id) is None:
        db.create_user([user_id,
        now.strftime("%Y-%m-%d"),
        message.from_user.first_name,
        '@' + message.from_user.username])
        await message.answer('<b>Добро пожаловать в мир обоев на телефон!\nВсе обои в данном боте были загружены людьми.</b>')
    await message.answer('Меню.', reply_markup=main_menu)


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
