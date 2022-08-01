from aiogram import Dispatcher
from aiogram import types
from aiohttp import ContentTypeError
from requests import delete
from tgbot.keyboards.inline import *
from tgbot.misc.states import Upload_wallpaper
from aiogram.dispatcher import FSMContext
from tgbot import db
from datetime import datetime
from tgbot.handlers.admin import bot
from aiogram.types import InputMediaPhoto

db = db.Data("tgbot/database/database.db")
now = datetime.now()

async def upload_wallpaper(call: types.CallbackQuery):
    await call.message.edit_text(
        '<b>Отправьте обои в формате гифки или изображения</b>'
        , reply_markup=main_menu_back)
    await Upload_wallpaper.media.set()

async def get_cats(user_id, mode):
    all = db.get_all_cat()
    spisok_keyboards = InlineKeyboardMarkup(row_width=2)
    now_filter = db.get_user_filters(user_id)
    for hq in all:
        if str(hq[0]) in now_filter.split(','):
            spisok_keyboards.insert(InlineKeyboardButton(f'✅ {hq[1]}', callback_data='filter' + str(hq[0])))
        else:
            spisok_keyboards.insert(InlineKeyboardButton(f'{hq[1]}', callback_data='filter' + str(hq[0])))
    if mode == 1:
        spisok_keyboards.insert(btn_back)
    else:
        spisok_keyboards.insert(filter_back)
    return spisok_keyboards

async def end_of_upload(message: types.Message, state: FSMContext):
    try:
        await state.update_data(media=message.animation.file_id)
    except:
        await state.update_data(media=message.photo[-1].file_id)
    all = db.get_all_cat()
    spisok_keyboards = InlineKeyboardMarkup(row_width=2)
    for hq in all:
        spisok_keyboards.insert(InlineKeyboardButton(f'{hq[1]}', callback_data='cat' + str(hq[0])))
    await message.answer(
        '<b>Выберите категорию!</b>'
        , reply_markup=spisok_keyboards)
    await Upload_wallpaper.next()

async def end_of_upload_last(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['cat'] = call.data.split('cat')[1]
        await call.message.delete()
        db.add_wallpaper( 
            [data['media'],
            call.from_user.id,
            now.strftime("%Y-%m-%d"),
            call.from_user.first_name,
            0,data['cat']])
    await call.message.answer(
        '<b>Обои успешно загружены, теперь они будут в каталоге бота!</b>'
        , reply_markup=main_menu_back)

async def filter_add(call: types.CallbackQuery):
    filter_id = call.data.split('filter')[1]
    now_filter = db.get_user_filters(call.from_user.id)
    if filter_id in now_filter.split(','):
        now_filter = now_filter.replace(',' + filter_id,'')
    else:
        now_filter += ',' + filter_id
    db.add_filter(now_filter,call.from_user.id)
    spisok_keyboards = await get_cats(call.from_user.id, 0)
    await call.message.edit_reply_markup(reply_markup=spisok_keyboards)
    
        


async def pre_filters(call: types.CallbackQuery):
    await call.message.edit_text('<b>Выберите фильтры для поиска обоев!</b>', reply_markup=filters_keyboard)    
                                          
async def filters(call: types.CallbackQuery):
    spisok_keyboards = await get_cats(call.from_user.id, 0)
    await call.message.edit_text('<b>Фильтры</b>', reply_markup=spisok_keyboards)

async def catalog(call: types.CallbackQuery):
    now_filter = db.get_user_filters(call.from_user.id)
    ids = db.get_all_ids(now_filter)
    if len(ids) != 0:
        await call.message.delete()
        wallpaper = db.take_wallpaper_by_id(ids[-1])[0]
        cat = db.get_cat_by_id(wallpaper[6])
        caption = f'<b>Айди - <i>{wallpaper[0]}</i>\
                    \nАвтор - <i>{wallpaper[4]}</i>\
                    \nДобавлено - <i>{wallpaper[3]}</i>\
                    \nКатегория - <i>{cat}</i>\
                    \nЛайков - <i>{wallpaper[5]}</i></b>'
        if call.from_user.id == int(wallpaper[2]):
            keyb = catalog_buttons_del
        else:
            keyb = catalog_buttons
        try:
            await call.message.answer_photo(
                wallpaper[1],
                caption=caption
                ,reply_markup=keyb)
        except:
            await call.message.answer_animation(
                wallpaper[1],
                caption=caption
                ,reply_markup=keyb)  
    else:
        await call.answer('Выберите фильтры для поиска!')


async def like(call: types.CallbackQuery):
    id = (call.message.caption).split(' - ')[1].split('Автор')[0]
    user_id = call.from_user.id
    wallpaper = db.take_wallpaper_by_id(id)[0]
    if db.check_like(user_id, id) is None:
        db.add_like(id, user_id)
        await call.message.edit_caption("<b>" + call.message.caption.replace(f'Лайков - {str(wallpaper[5])}',f'Лайков - {str(wallpaper[5]+1)}') + "</b>"
        , reply_markup=catalog_buttons)
        check = db.get_notif_user(wallpaper[2])
        if check == 0:
            await bot.send_message(wallpaper[2], f'<b>{call.from_user.first_name} поставил(а) вам лайк.</b>')
        await call.answer('Вы поставили лайк!')
    else:
        db.remove_like(id, user_id)
        await call.answer('Вы убрали лайк!')
        await call.message.edit_caption("<b>" + call.message.caption.replace(f'Лайков - {str(wallpaper[5])}',f'Лайков - {str(wallpaper[5]-1)}') + "</b>"
        , reply_markup=catalog_buttons)

async def next_wall(call: types.CallbackQuery):
    id = int((call.message.caption).split(' - ')[1].split('Автор')[0])
    now_filter = db.get_user_filters(call.from_user.id)
    ids = db.get_all_ids(now_filter)
    next_id = ids.index(id)
    try:
        wallpaper = db.take_wallpaper_by_id(ids[next_id + 1])[0]
    except:
        wallpaper = db.take_wallpaper_by_id(ids[0])[0]
    cat = db.get_cat_by_id(wallpaper[6])
    caption = f'<b>Айди - <i>{wallpaper[0]}</i>\
                \nАвтор - <i>{wallpaper[4]}</i>\
                \nДобавлено - <i>{wallpaper[3]}</i>\
                \nКатегория - <i>{cat}</i>\
                \nЛайков - <i>{wallpaper[5]}</i></b>'
    if call.from_user.id == int(wallpaper[2]):
        keyb = catalog_buttons_del
    else:
        keyb = catalog_buttons
    link = InputMediaPhoto(wallpaper[1])
    try:
        await call.message.edit_media(media = link)
        await call.message.edit_caption(caption=caption, reply_markup=keyb)
    except:
        await call.message.delete()
        await call.message.answer_animation(
            wallpaper[1],
            caption=caption
            ,reply_markup=keyb)   


async def prev_wall(call: types.CallbackQuery):
    id = int((call.message.caption).split(' - ')[1].split('Автор')[0])
    now_filter = db.get_user_filters(call.from_user.id)
    ids = db.get_all_ids(now_filter)
    prev_id = ids.index(id)
    wallpaper = db.take_wallpaper_by_id(ids[prev_id - 1])[0]
    cat = db.get_cat_by_id(wallpaper[6])
    caption = f'<b>Айди - <i>{wallpaper[0]}</i>\
                \nАвтор - <i>{wallpaper[4]}</i>\
                \nДобавлено - <i>{wallpaper[3]}</i>\
                \nКатегория - <i>{cat}</i>\
                \nЛайков - <i>{wallpaper[5]}</i></b>'
    if call.from_user.id == int(wallpaper[2]):
        keyb = catalog_buttons_del
    else:
        keyb = catalog_buttons
    link = InputMediaPhoto(wallpaper[1])
    try:
        await call.message.edit_media(media = link)
        await call.message.edit_caption(caption=caption, reply_markup=keyb)
    except:
        await call.message.delete()
        await call.message.answer_animation(
            wallpaper[1],
            caption=caption
            ,reply_markup=keyb)   

async def profile(call: types.CallbackQuery):
    user_id = call.from_user.id
    notifs = db.get_notif_user(user_id)
    if notifs == 0:
        text = 'включены'
    else:
        text = 'выключены'
    await call.message.edit_text(f'<b>Ваша статистика.\n\
                                    \n  -  Айди - {user_id}\
                                    \n  -  Имя - <i>{call.from_user.first_name}</i>\
                                    \n  -  Вы с нами с - <i>{db.get_user_date(user_id)}</i>\
                                    \n  -  Вы загрузили - {db.get_user_wallpapers(user_id)} обоев.\
                                    \n  -  У вас {db.get_user_likes(user_id)} лайков.\
                                    \n  -  Уведомления - {text}</b>', reply_markup=profile_menu)

async def notifications(call: types.CallbackQuery):
    user_id = call.from_user.id
    notifs = db.get_notif_user(user_id)
    if notifs == 0:
        await call.message.edit_text('<b>'+
            call.message.text.replace('включены','выключены') + '</b>', reply_markup=profile_menu)
        db.change_notif_user(1,user_id)
    else:
        await call.message.edit_text('<b>'+
            call.message.text.replace('выключены','включены') + '</b>', reply_markup=profile_menu)
        db.change_notif_user(0,user_id)

async def del_wall(call: types.CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=yes_or_no_keyboard)

async def yes_delete(call: types.CallbackQuery):
    db.del_wallpapers_by_id((call.message.caption).split(' - ')[1].split('Автор')[0])
    await call.answer('Обои успешно удалены!')
    await call.message.delete()
    await call.message.answer(
        f'Меню.', reply_markup=main_menu)


async def no_delete(call: types.CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=catalog_buttons_del)

async def back(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer(
        f'Меню.', reply_markup=main_menu)

async def back_to_filter(call: types.CallbackQuery):
    await call.message.edit_text('<b>Выберите фильтры для поиска обоев!</b>', reply_markup=filters_keyboard)

async def inf(call: types.CallbackQuery):
    walls = db.count_wallpapers()
    users = db.get_all_users()
    get_top = db.get_top_users()
    await call.message.edit_text(
        f'<b><i>Топ пользователей</i></b>\n'
        f'<b>   {get_top[0][0]}    ⇝  {get_top[0][1]}</b>\n'
        f'<b>   {get_top[1][0]}    ⇝  {get_top[1][1]}</b>\n'
        f'<b>   {get_top[2][0]}    ⇝  {get_top[2][1]}</b>\n'
        f'<b>   {get_top[3][0]}    ⇝  {get_top[3][1]}</b>\n'
        f'<b>   {get_top[4][0]}    ⇝  {get_top[4][1]}</b>\n\n'
        f'<b><i>Общая статистика</i></b>\n'
        f'<b>   Всего загрузили    ⇝ {walls}</b>\n'
        f'<b>   Всего пользователей    ⇝ {users}</b>\n\n'
        f'<b><i>По всем вопросам - @xartd012</i></b>\n'
        , reply_markup=main_menu_back)



def register_calls(dp: Dispatcher):

    dp.register_callback_query_handler(upload_wallpaper, 
    lambda call: call.data == 'upload', state='*')

    dp.register_callback_query_handler(notifications, 
    lambda call: call.data == 'notif', state='*')
 
    dp.register_callback_query_handler(back, 
    lambda call: call.data == 'back_to_main', state='*')

    dp.register_callback_query_handler(catalog, 
    lambda call: call.data == 'catalog', state='*')

    dp.register_callback_query_handler(like, 
    lambda call: call.data == 'like_wallpaper', state='*')

    dp.register_callback_query_handler(inf, 
    lambda call: call.data == 'information', state='*')

    dp.register_callback_query_handler(next_wall, 
    lambda call: call.data == 'next_wallpaper', state='*')

    dp.register_callback_query_handler(prev_wall, 
    lambda call: call.data == 'prev_wallpaper', state='*')

    dp.register_callback_query_handler(profile, 
    lambda call: call.data == 'profile', state='*')

    dp.register_callback_query_handler(del_wall, 
    lambda call: call.data == 'del_wallpaper', state='*')

    dp.register_callback_query_handler(yes_delete, 
    lambda call: call.data == 'yes', state='*')

    dp.register_callback_query_handler(no_delete, 
    lambda call: call.data == 'no', state='*')

    dp.register_callback_query_handler(pre_filters, 
    lambda call: call.data == 'pre_filters', state='*')

    dp.register_callback_query_handler(filters, 
    lambda call: call.data == 'filters', state='*')

    dp.register_callback_query_handler(back_to_filter, 
    lambda call: call.data == 'back_to_filter', state='*')

    dp.register_callback_query_handler(end_of_upload_last, 
    lambda call: call.data.startswith('cat'), state=Upload_wallpaper.cat)

    dp.register_callback_query_handler(filter_add, 
    lambda call: call.data.startswith('filter'), state='*')

    dp.register_message_handler(end_of_upload,
    content_types=['photo','animation'],
    state=Upload_wallpaper.media)
