import telebot

from src.configuration import *
from src.bot_panels import *
from src.controller import *

from src.planet.warehouse import *
from src.converter import *
from src.shuttle import Shuttle


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
            controller.users[call.message.chat.id].planet = _planet
            controller.users[call.message.chat.id].state == State.RESEARCH
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
        controller.users[message.from_user.id].state = State.MENU
        name = controller.users[message.from_user.id].name
        name_for_news = '*{}*'.format(name)
        # controller.restore_bd()
        if name != ANONYMOUS_USER:
            name_for_news = 'Пользователь *{}*'.format(name)
        teacher_text = '{} вызвал справку.'.format(name_for_news)
        bot.send_message(TEACHER_CHANNEL, teacher_text, parse_mode="Markdown")
        bot.send_message(message.from_user.id, HELP_TEXT, parse_mode="Markdown")
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
        elif controller.users[message.from_user.id].state == State.SETTINGS:
            controller.users[message.from_user.id].state = State.MENU
            text = '*{}* = {}'.format(message.from_user.id, message.text)
            # controller.users[message.from_user.id].name = message.text
            controller.set_user(message.from_user.id, Property.NAME, message.text)
            bot.send_message(TEACHER_CHANNEL, text,  parse_mode="Markdown")
        # Режим ИССЛЕДОВАНИЯ
        elif controller.users[message.from_user.id].state == State.RESEARCH:
            # Программа для учителей
            name = controller.users[message.from_user.id].name
            name_for_news = '*{}*'.format(name)
            news_text = '{}:\n```{}```'.format(name_for_news, '\n' + message.text)
            bot.send_message(TEACHER_CHANNEL, news_text, parse_mode="Markdown")

            # Отправляем диоход
            controller.users[message.from_user.id].state = State.RESEARCH
            user_planet = controller.users[message.from_user.id].planet
            user_shuttle = Shuttle(user_planet)
            try:
                # Выполняем программу
                user_program = convert_to_lines(message.text)
                user_shuttle.execute(user_program)

                text_for_student = '*Диоход завершил свою миссию!*\n'
                unique_amount = len(user_shuttle.explored_cells)
                text_for_student += 'Cфотографировано различных клеток планеты: {} шт.\n'.format(unique_amount)
                if len(user_shuttle.memory) == 0:
                    text_for_student += 'Не было получено ни одной фотографии'
                else:
                    text_for_student += 'Были получены следующие фотографии:'
                # Результат для детей
                bot.send_message(message.from_user.id, text_for_student, parse_mode="Markdown")

                teacher_photos = []
                for _photo in user_shuttle.memory:
                    bot.send_photo(message.from_user.id, _photo.get_image())
                    teacher_photos.append(_photo.get_description())
                bot.send_message(message.from_user.id, "Выберите в меню дальнейшее действие", parse_mode="Markdown")

                # Результат для учителей
                not_done = []
                for artifact_address in user_shuttle.not_photographed:
                    artifact = user_planet.area[artifact_address[0]][artifact_address[1]]
                    not_done.append(artifact.get_description())
                news_text = '{} получил результат:\n-----\n_{}_'.format(name_for_news, text_for_student)
                news_text += '\n{}'.format(str(teacher_photos))
                news_text += '\n-----\n *Не было сфотографировано:* {}'.format(str(not_done))
                bot.send_message(TEACHER_CHANNEL, news_text, parse_mode="Markdown")

            except CompilationError as err:
                error_text = """*Ошибка в коде программы:*\n{}""".format(err.message)
                bot.send_message(message.from_user.id, error_text, parse_mode="Markdown")

                news_text = '{} получил результат:\n```{}```'.format(name_for_news, '\n' + error_text)
                bot.send_message(TEACHER_CHANNEL, news_text, parse_mode="Markdown")
            except ActionError as err:
                error_text = """*Получено экстренное сообщение от диохода:*\n{}""".format(err.message)
                bot.send_message(message.from_user.id, error_text, parse_mode="Markdown")

                news_text = '{} получил результат:\n```{}```'.format(name_for_news, '\n' + error_text)
                bot.send_message(TEACHER_CHANNEL, news_text, parse_mode="Markdown")
            except PlanetError as err:
                error_text = """{}""".format(err.message)
                bot.send_message(message.from_user.id, error_text, parse_mode="Markdown")

                news_text = '{} получил результат:\n```{}```'.format(name_for_news, '\n' + error_text)
                bot.send_message(TEACHER_CHANNEL, news_text, parse_mode="Markdown")
            except Exception as err:
                bot.send_message(message.from_user.id, "Ошибка в программе", parse_mode="Markdown")
        else:
            bot.send_message(message.from_user.id, 'Выберите действие в меню')


bot.polling()
