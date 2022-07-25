from aiogram import types, Dispatcher
from tgbot.keyboards.inline import *

async def bot_echo(message: types.Message):
    await message.answer('Я не очень понял твое сообщение, вот главное меню', reply_markup=main_menu)


def register_echo(dp: Dispatcher):
    dp.register_message_handler(bot_echo)
