from aiogram import Bot, Dispatcher
from aiogram.types import Message
from tgbot import db
from tgbot.config import load_config

config = load_config(".env")
bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
db = db.Data("tgbot/database/database.db")

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
