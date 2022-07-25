from email import message
from aiogram import Dispatcher
from aiogram import types
from aiohttp import ContentTypeError
from tgbot.keyboards.inline import *
from tgbot.misc.states import Upload_wallpaper
from aiogram.dispatcher import FSMContext
from tgbot import db
from datetime import datetime

db = db.Data("tgbot/database/database.db")
now = datetime.now()

async def upload_wallpaper(call: types.CallbackQuery):
    await call.message.edit_text(
        '<b>Отправьте обои в формате гифки или изображения</b>'
        , reply_markup=main_menu_back)
    await Upload_wallpaper.media.set()

async def end_of_upload(message: types.Message, state: FSMContext):
    try:
        db.add_wallpaper(
            [message.animation.file_id,
            message.from_user.id,
            now.strftime("%Y-%m-%d"),
            message.from_user.first_name,
            0])
    except:
        db.add_wallpaper(
            [message.photo[-1].file_id,
            message.from_user.id,
            now.strftime("%Y-%m-%d"),
            message.from_user.first_name,
            0])
    await message.answer(
        '<b>Обои успешно загружены, теперь они будут в каталоге бота!</b>'
        , reply_markup=main_menu_back)
    await state.finish()


async def catalog(call: types.CallbackQuery):
    await call.message.delete()
    wallpaper = db.take_wallpaper(db.check_anti_id(call.from_user.id))[0]
    db.add_anti_id(wallpaper[0], call.from_user.id)
    try:
        await call.message.answer_photo(
            wallpaper[1],
            caption=f'<b>Айди - <i>{wallpaper[0]}</i>\nАвтор - <i>{wallpaper[4]}</i>\nДобавлено - <i>{wallpaper[3]}</i>\nЛайков - <i>{wallpaper[5]}</i></b>'
            ,reply_markup=catalog_buttons)
    except:
        await call.message.answer_animation(
            wallpaper[1],
            caption=f'<b>Айди - <i>{wallpaper[0]}</i>\nАвтор - <i>{wallpaper[4]}</i>\nДобавлено - <i>{wallpaper[3]}</i>\nЛайков - <i>{wallpaper[5]}</i></b>'
            ,reply_markup=catalog_buttons)      
    
async def like(call: types.CallbackQuery):
    id = (call.message.caption).split(' - ')[1][0]
    user_id = call.from_user.id
    if db.check_like(user_id, id) is None:
        db.add_like(id)
        db.add_user_likes(user_id, id)
        wallpaper = db.take_wallpaper_by_id(id)[0]
        await call.message.delete()
        try:
            await call.message.answer_photo(
                wallpaper[1],
                caption=f'<b>Айди - <i>{wallpaper[0]}</i>\nАвтор - <i>{wallpaper[4]}</i>\nДобавлено - <i>{wallpaper[3]}</i>\nЛайков - <i>{wallpaper[5]}</i></b>'
                ,reply_markup=catalog_buttons)
        except:
            await call.message.answer_animation(
                wallpaper[1],
                caption=f'<b>Айди - <i>{wallpaper[0]}</i>\nАвтор - <i>{wallpaper[4]}</i>\nДобавлено - <i>{wallpaper[3]}</i>\nЛайков - <i>{wallpaper[5]}</i></b>'
                ,reply_markup=catalog_buttons)
    else:
        await call.answer('Вы уже поставили лайк!')

async def back(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer(
        'Меню.', reply_markup=main_menu)

async def inf(call: types.CallbackQuery):
    await call.message.edit_text('<b>Данный бот - это аналог wallpaper engine, но в телеграме и для телефона, буду его обновлять, добавляйте свои обои!</b>', reply_markup=main_menu_back)



def register_calls(dp: Dispatcher):

    dp.register_callback_query_handler(upload_wallpaper, 
    lambda call: call.data == 'upload', state='*')
 
    dp.register_callback_query_handler(back, 
    lambda call: call.data == 'back_to_main', state='*')

    dp.register_callback_query_handler(catalog, 
    lambda call: call.data == 'catalog', state='*')

    dp.register_callback_query_handler(like, 
    lambda call: call.data == 'like_wallpaper', state='*')

    dp.register_callback_query_handler(inf, 
    lambda call: call.data == 'information', state='*')

    dp.register_message_handler(end_of_upload,
    content_types=['photo','animation'],
    state=Upload_wallpaper.media)
