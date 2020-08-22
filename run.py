import telebot

from configuration import *
from bot_panels import *


bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(
        message.chat.id,
        """\U0001F44B Приветствуем вас на виртуальном космодроме!
        \n\U0001F680 Отсюда вы можете посылать вирутальные аппараты для исследования виртуальных планет.
        \n\U0001F4F0 Если обнаружите что-то интересное - обязательно опубликуйте новость, чтобы вирутальное научное сообщество узнало об этом.""",
        parse_mode="Markdown",
        reply_markup=main_panel)


bot.polling()
