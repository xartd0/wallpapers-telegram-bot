from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
   

# Главное меню
btn_1 = InlineKeyboardButton('📚 Каталог', callback_data='catalog')
btn_2 = InlineKeyboardButton('📂 Загрузить', callback_data='upload')
btn_3 = InlineKeyboardButton('❔ Информация', callback_data='information')
btn_4 = InlineKeyboardButton('💻 Профиль', callback_data='profile')
main_menu = InlineKeyboardMarkup(row_width=2).add(btn_1, btn_2, btn_4, btn_3)

# Обратно в главное меню
btn_back = InlineKeyboardButton('🔙 Обратно', callback_data='back_to_main')
main_menu_back = InlineKeyboardMarkup().add(btn_back)


# Кнопки в каталоге общие
like_btn = InlineKeyboardButton('❤ Лайк', callback_data='like_wallpaper')
back_btn = InlineKeyboardButton('◀', callback_data='prev_wallpaper')
next_btn = InlineKeyboardButton('▶', callback_data='next_wallpaper')
catalog_buttons = InlineKeyboardMarkup(2).add(back_btn, next_btn, like_btn ,btn_back)


notif_btn = InlineKeyboardButton('📨 Уведомления', callback_data='notif')
profile_menu = InlineKeyboardMarkup(row_width=1).add(notif_btn, btn_back)
