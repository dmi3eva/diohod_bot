from telebot import types


from settings import *

# Основное меню
launch_button = types.KeyboardButton(text='\U0001F680 {}'.format(LAUNCH_BUTTON_TEXT.capitalize()))
news_button = types.KeyboardButton(text='\U0001F4F0 {}'.format(PUBLISH_BUTTON_TEXT.capitalize()))
help_button = types.KeyboardButton(text='\U0001F691 {}'.format(HELP_BUTTON_TEXT.capitalize()))


main_panel = types.ReplyKeyboardMarkup(True, False, row_width=2)
main_panel.add(launch_button)
main_panel.add(news_button, help_button)