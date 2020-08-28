import telebot

from configuration import *
from bot_panels import *
from controller import *
from planet import *
from planet.warehouse import *
from converter import *


bot = telebot.TeleBot(API_TOKEN)
controller = Controller()


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(
        message.chat.id,
        """\U0001F44B Приветствуем вас на виртуальном космодроме!
        \n\U0001F680 Отсюда вы можете посылать вирутальные аппараты для исследования виртуальных планет.
        \n\U0001F4F0 Если обнаружите что-то интересное - обязательно опубликуйте новость, чтобы вирутальное научное сообщество узнало об этом.""",
        parse_mode="Markdown",
        reply_markup=main_panel)
    controller.restore_bd()


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    for _data, _planet in CALL_PLANET_CORRESPONDENCE.items():
        if call.data == _data:
            controller.users[call.message.from_user.id].planet = _planet
            controller.users[call.message.from_user.id].state == State.RESEARCH
            bot.send_message(call.message.chat.id, _planet.mission.text, parse_mode="Markdown")
            illustration = _planet.mission.get_illustration()
            if illustration is not None:
                bot.send_photo(call.message.chat.id, illustration)
            break


@bot.message_handler(content_types=['text'])
def start(message):
    if LAUNCH_BUTTON_TEXT in message.text.lower():
        bot.send_message(message.from_user.id, 'На какую планету отправить ракету с диоходом?', reply_markup=planet_panel)
        controller.users[message.from_user.id].state = State.RESEARCH
    elif HELP_BUTTON_TEXT in message.text.lower():
        bot.send_message(message.from_user.id, 'Помощь')
        controller.users[message.from_user.id].state = State.HELP
    elif PUBLISH_BUTTON_TEXT in message.text.lower():
        bot.send_message(
            message.from_user.id,
            """Что будем сообщать миру?
            \nВведите текст и не забудьте указать, какой планеты касается ваше открытие."""
        )
        controller.users[message.from_user.id].state = State.NEWS
        bot.send_message(NEWS_CHANNEL, message.from_user.id)
    elif SETTINGS_BUTTON_TEXT in message.text.lower():
        bot.send_message(message.from_user.id, 'Введите, пожалуйста, свою фамилию и имя')
        controller.users[message.from_user.id].state = State.SETTINGS
    else:
        # Режим НОВОСТЕЙ
        if controller.users[message.from_user.id].state == State.NEWS:
            name = controller.users[message.from_user.id].name
            name_for_news = '*{}*'.format(name)
            # controller.restore_bd()
            if name != ANONYMOUS_USER:
                name_for_news = 'Пользователь *{}*'.format(name)
            news_text = '{} только что сообщил новость:\n_\"{}\"_'.format(name_for_news, message.text)
            bot.send_message(NEWS_CHANNEL, news_text,  parse_mode="Markdown")
            teacher_text = '*{}* ({}):\nНОВОСТЬ\n_\"{}\"_'.format(message.from_user.id, name, message.text)
            bot.send_message(TEACHER_CHANNEL, teacher_text, parse_mode="Markdown")
        # Режим РЕГИСТРАЦИИ
        if controller.users[message.from_user.id].state == State.SETTINGS:
            controller.users[message.from_user.id].state = State.MENU
            text = '*{}* = {}'.format(message.from_user.id, message.text)
            # controller.users[message.from_user.id].name = message.text
            controller.set_user(message.from_user.id, Property.NAME, message.text)
            bot.send_message(TEACHER_CHANNEL, text,  parse_mode="Markdown")


bot.polling()
