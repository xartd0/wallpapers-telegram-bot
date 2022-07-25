from aiogram import Dispatcher
from aiogram.types import Message


async def admin_start(message: Message):
    await message.reply("Тут будет админ_панель")


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["admin_panel"], state="*", is_admin=True)
