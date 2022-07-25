from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
    

# Главное меню
btn_1 = InlineKeyboardButton('📚 Каталог', callback_data='catalog')
btn_2 = InlineKeyboardButton('📂 Загрузить', callback_data='upload')
btn_3 = InlineKeyboardButton('❔ Информация', callback_data='information')
main_menu = InlineKeyboardMarkup(row_width=2).add(btn_1, btn_2, btn_3)

# Обратно в главное меню
btn_back = InlineKeyboardButton('🔙 Обратно', callback_data='back_to_main')
main_menu_back = InlineKeyboardMarkup().add(btn_back)

# Кнопки в каталоге
like_btn = InlineKeyboardButton('❤ Лайк', callback_data='like_wallpaper')
next_btn = InlineKeyboardButton('⏩ Дальше', callback_data='catalog')
catalog_buttons = InlineKeyboardMarkup(2).add(like_btn, next_btn, btn_back)