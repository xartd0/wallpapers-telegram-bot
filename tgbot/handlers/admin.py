from aiogram import Dispatcher
from aiogram.types import Message
from tgbot.handlers.imports import *

async def admin_spam(message: Message):
    users = db.get_all_users_ids()
    for user in users:
        print(user)
        try:
            await bot.send_message(user, message.get_args())
        except:
            pass
    await message.answer(f'Рассылка прошла успешно! ({len(users)})')



def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_spam, commands=["spam"], state="*", is_admin=True)
