from telebot import types


from settings import *

# Основное меню
launch_button = types.KeyboardButton(text='\U0001F680 {}'.format(LAUNCH_BUTTON_TEXT.capitalize()))
news_button = types.KeyboardButton(text='\U0001F4F0 {}'.format(PUBLISH_BUTTON_TEXT.capitalize()))
help_button = types.KeyboardButton(text='\U0001F691 {}'.format(HELP_BUTTON_TEXT.capitalize()))
settings_button = types.KeyboardButton(text='\U0001F6AA {}'.format(SETTINGS_BUTTON_TEXT.capitalize()))

main_panel = types.ReplyKeyboardMarkup(True, False, row_width=3)
main_panel.add(launch_button)
main_panel.add(news_button, help_button, settings_button)

# Меню планет
planet_button_01 = types.InlineKeyboardButton(text='\U0001F30D Планета 01', callback_data='planet_01')
planet_button_02 = types.InlineKeyboardButton(text='\U0001F30D Планета 02', callback_data='planet_02')
planet_button_03 = types.InlineKeyboardButton(text='\U0001F30D Планета 03', callback_data='planet_03')

planet_button_04 = types.InlineKeyboardButton(text='\U0001F30E Планета 04', callback_data='planet_04')
planet_button_05 = types.InlineKeyboardButton(text='\U0001F30E Планета 05', callback_data='planet_05')
planet_button_06 = types.InlineKeyboardButton(text='\U0001F30E Планета 06', callback_data='planet_06')

planet_button_07 = types.InlineKeyboardButton(text='\U0001F30F Планета 07', callback_data='planet_07')
planet_button_08 = types.InlineKeyboardButton(text='\U0001F30F Планета 08', callback_data='planet_08')
planet_button_09 = types.InlineKeyboardButton(text='\U0001F30F Планета 09', callback_data='planet_09')

planet_button_10 = types.InlineKeyboardButton(text='\U0001FA90 Планета 10', callback_data='planet_10')
planet_button_11 = types.InlineKeyboardButton(text='\U0001FA90 Планета 11', callback_data='planet_11')
planet_button_12 = types.InlineKeyboardButton(text='\U0001FA90 Планета 12', callback_data='planet_12')

planet_panel = types.InlineKeyboardMarkup(row_width=3)
planet_panel.add(planet_button_01, planet_button_02, planet_button_03)
planet_panel.add(planet_button_04, planet_button_05, planet_button_06)
planet_panel.add(planet_button_07, planet_button_08, planet_button_09)
planet_panel.add(planet_button_10, planet_button_11, planet_button_12)
