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
    ids = db.get_all_ids()
    wallpaper = db.take_wallpaper_by_id(ids[-1])[0]
    caption = f'<b>Айди - <i>{wallpaper[0]}</i>\
                \nАвтор - <i>{wallpaper[4]}</i>\
                \nДобавлено - <i>{wallpaper[3]}</i>\
                \nЛайков - <i>{wallpaper[5]}</i></b>'
    try:
        await call.message.answer_photo(
            wallpaper[1],
            caption=caption
            ,reply_markup=catalog_buttons)
    except:
        await call.message.answer_animation(
            wallpaper[1],
            caption=caption
            ,reply_markup=catalog_buttons)    


async def like(call: types.CallbackQuery):
    id = (call.message.caption).split(' - ')[1].split('Автор')[0]
    user_id = call.from_user.id
    wallpaper = db.take_wallpaper_by_id(id)[0]
    if db.check_like(user_id, id) is None:
        db.add_like(id, user_id)
        await call.message.edit_caption("<b>" + call.message.caption.replace(f'Лайков - {str(wallpaper[5])}',f'Лайков - {str(wallpaper[5]+1)}') + "</b>"
        , reply_markup=catalog_buttons)
        await call.answer('Вы поставили лайк!')
    else:
        db.remove_like(id, user_id)
        await call.answer('Вы убрали лайк!')
        await call.message.edit_caption("<b>" + call.message.caption.replace(f'Лайков - {str(wallpaper[5])}',f'Лайков - {str(wallpaper[5]-1)}') + "</b>"
        , reply_markup=catalog_buttons)

async def next_wall(call: types.CallbackQuery):
    await call.message.delete()
    id = int((call.message.caption).split(' - ')[1].split('Автор')[0])
    ids = db.get_all_ids()
    next_id = ids.index(id)
    try:
        wallpaper = db.take_wallpaper_by_id(ids[next_id + 1])[0]
    except:
        wallpaper = db.take_wallpaper_by_id(ids[0])[0]
    caption = f'<b>Айди - <i>{wallpaper[0]}</i>\
                \nАвтор - <i>{wallpaper[4]}</i>\
                \nДобавлено - <i>{wallpaper[3]}</i>\
                \nЛайков - <i>{wallpaper[5]}</i></b>'
    try:
        await call.message.answer_photo(
            wallpaper[1],
            caption=caption
            ,reply_markup=catalog_buttons)
    except:
        await call.message.answer_animation(
            wallpaper[1],
            caption=caption
            ,reply_markup=catalog_buttons)   

async def prev_wall(call: types.CallbackQuery):
    await call.message.delete()
    id = int((call.message.caption).split(' - ')[1].split('Автор')[0])
    ids = db.get_all_ids()
    prev_id = ids.index(id)
    wallpaper = db.take_wallpaper_by_id(ids[prev_id - 1])[0]
    caption = f'<b>Айди - <i>{wallpaper[0]}</i>\
                \nАвтор - <i>{wallpaper[4]}</i>\
                \nДобавлено - <i>{wallpaper[3]}</i>\
                \nЛайков - <i>{wallpaper[5]}</i></b>'
    try:
        await call.message.answer_photo(
            wallpaper[1],
            caption=caption
            ,reply_markup=catalog_buttons)
    except:
        await call.message.answer_animation(
            wallpaper[1],
            caption=caption
            ,reply_markup=catalog_buttons)   



async def back(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer(
        f'Меню.', reply_markup=main_menu)

async def inf(call: types.CallbackQuery):
    walls = db.count_wallpapers()
    users = db.get_all_users()
    await call.message.edit_text(f'<b>Данный бот - это аналог wallpaper engine, но в телеграме и для телефона, буду его обновлять, добавляйте свои обои!\n\nСтатистика.\nЗагрузили - {walls} обоев.\nВсего - {users} пользователей.</b>', reply_markup=main_menu_back)



def register_calls(dp: Dispatcher):

    dp.register_callback_query_handler(upload_wallpaper, 
    lambda call: call.data == 'upload', state='*')
 
    dp.register_callback_query_handler(back, 
    lambda call: call.data == 'back_to_main', state='*')

    dp.register_callback_query_handler(catalog, 
    lambda call: call.data == 'catalog', state='*', is_admin=True)

    dp.register_callback_query_handler(like, 
    lambda call: call.data == 'like_wallpaper', state='*')

    dp.register_callback_query_handler(inf, 
    lambda call: call.data == 'information', state='*')

    dp.register_callback_query_handler(next_wall, 
    lambda call: call.data == 'next_wallpaper', state='*')

    dp.register_callback_query_handler(prev_wall, 
    lambda call: call.data == 'prev_wallpaper', state='*')

    dp.register_message_handler(end_of_upload,
    content_types=['photo','animation'],
    state=Upload_wallpaper.media)
