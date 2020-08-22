from telebot import types

# Основное меню
launch_button = types.InlineKeyboardButton(text='\U0001F680 Запустить виртуальную ракету', callback_data='lunch')
news_button = types.InlineKeyboardButton(text='\U0001F4F0 Опубликовать новость', callback_data='publish')
help_button = types.InlineKeyboardButton(text='\U0001F691 Помощь', callback_data='help')


main_panel = types.ReplyKeyboardMarkup(True, False, row_width=2)
main_panel.add(launch_button)
main_panel.add(news_button, help_button)