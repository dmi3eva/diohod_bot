import telebot

from configuration import *
from bot_panels import *
from controller import *
from planet import *
from executer import *


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
    controller.current_state[message.user.id] = State.MENU


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    print("THIS")



@bot.message_handler(content_types=['text'])
def start(message):
    if LAUNCH_BUTTON_TEXT in message.text.lower():
        bot.send_message(message.from_user.id, 'Запуск')
        print(controller.current_state)
        controller.current_state[message.user.id] = State.RESEARCH
    if HELP_BUTTON_TEXT in message.text.lower():
        bot.send_message(message.from_user.id, 'Помощь')
        print(controller.current_state)
        controller.current_state[message.user.id] = State.HELP
    if PUBLISH_BUTTON_TEXT in message.text.lower():
        bot.send_message(message.from_user.id, 'Новости!')
        print(controller.current_state)
        controller.current_state[message.user.id] = State.NEWS

bot.polling()
