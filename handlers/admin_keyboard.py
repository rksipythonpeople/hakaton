from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

button_add_admin = KeyboardButton('Добавить админа')
button_del_admin = KeyboardButton('Удалить админа')
button_add_helper = KeyboardButton('Добавить хелпера')
button_del_helper = KeyboardButton('Удалить хелпера')
button_all_admin = KeyboardButton("Все админы")
admin_panel = ReplyKeyboardMarkup()
admin_panel.add(button_add_admin,button_add_helper,button_del_admin,button_del_helper,button_all_admin)

cancel_button = KeyboardButton('Отмена')
cancel_panel = ReplyKeyboardMarkup()
cancel_panel.add(cancel_button)