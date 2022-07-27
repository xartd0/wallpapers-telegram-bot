from aiogram import types, Dispatcher
from tgbot.keyboards.inline import *
from tgbot.handlers.user import *

async def bot_echo(message: types.Message):
    await message.answer('Я не понял твое сообщение!', reply_markup=types.ReplyKeyboardRemove())
    await user_start(message)


def register_echo(dp: Dispatcher):
    dp.register_message_handler(bot_echo)
