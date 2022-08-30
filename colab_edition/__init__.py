from typing import *
from base64 import b64encode
from IPython.display import Image, display, HTML, Markdown

from diohod_bot.src.planet.warehouse import *
from diohod_bot.src.shuttle import Shuttle
from diohod_bot.src.converter import *
from diohod_bot.src.error import *
from diohod_bot.src.utils import *

PLANETS = [None, planet_01, planet_02, planet_03, planet_04, planet_05, planet_06, planet_07, planet_08, planet_09]


def render_photo(path) -> NoReturn:
    try:
        if path:
            root_path = str(path).split('\\')[-1].split('/')[-1]
            if 'artifacts' in path:
                colab_path = "diohod_bot/img/artifacts/" + root_path
            else:
                colab_path = "diohod_bot/img/missions/" + root_path
            img = open(colab_path, 'rb').read()
    except:
        img = open('diohod_bot/img/other/error_with_text.png', 'rb').read()
    data = 'data:image/jpeg;base64,' + b64encode(img).decode()
    display(HTML(f"<img src='{data}' width='140'>"))


def go(mission_number: int, program: str) -> NoReturn:
    try:
        user_planet = PLANETS[mission_number]
        user_shuttle = Shuttle(user_planet)
        user_program = convert_to_lines(program)
        user_shuttle.execute(user_program)

        text_for_student = '<b>Диоход завершил свою миссию!</b><br>'
        unique_amount = len(user_shuttle.explored_cells)
        text_for_student += 'Cфотографировано различных клеток планеты: {} шт.<br>'.format(unique_amount)
        if len(user_shuttle.memory) == 0:
            text_for_student += 'Не было получено ни одной фотографии'
        else:
            text_for_student += 'Были получены следующие фотографии:'
        display(HTML(text_for_student))

        for ind, _photo in enumerate(user_shuttle.memory):
            display(HTML(f"<b>№{ind + 1}</b>"))
            render_photo(_photo.img_path)
    except CompilationError as err:
        error_text = """<b>Ошибка в коде программы:</b><br>{}""".format(err.message)
        display(HTML(error_text))
    except ActionError as err:
        error_text = """<b>Получено экстренное сообщение от диохода:</b><br>{}""".format(err.message)
        display(HTML(error_text))
    except PlanetError as err:
        error_text = """{}""".format(err.message)
        display(HTML(error_text))
    except Exception as err:
        render_photo(None)


def task(mission_number: int) -> NoReturn:
    try:
        user_planet = PLANETS[mission_number]
        mission = user_planet.mission
        print(mission.text)
        # display(f"{Markdown(mission.text)}")
        render_photo(mission.ill_path)
    except:
        print("На эту планету вам пока нельзя!")




# img = open('diohod_bot/img/artifacts/dino.png', 'rb').read()
# go(1, "move()\nrotate()\nphoto()")
