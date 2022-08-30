from typing import *
from base64 import b64encode
from IPython.display import Image, display, HTML

from planet.warehouse import *
from shuttle import Shuttle
from converter import *
from utils import *

PLANETS = [None, planet_01, planet_02, planet_03, planet_04, planet_05, planet_06, planet_07, planet_08, planet_09]


def render_photo(path):
    try:
        img = open(path, 'rb').read()
    except:
        img = open('diohod_bot/img/other/error_with_text.png', 'rb').read()
    data_url = 'data:image/jpeg;base64,' + b64encode(img).decode()
    return data_url


def go(mission_number: int, program: str) -> NoReturn:
    try:
        user_planet = PLANETS[mission_number]
        user_shuttle = Shuttle(user_planet)
        user_program = convert_to_lines(program)
        user_shuttle.execute(user_program)

        text_for_student = '<b>Диоход завершил свою миссию!</b>\n'
        unique_amount = len(user_shuttle.explored_cells)
        text_for_student += 'Cфотографировано различных клеток планеты: {} шт.\n'.format(unique_amount)
        if len(user_shuttle.memory) == 0:
            text_for_student += 'Не было получено ни одной фотографии'
        else:
            text_for_student += 'Были получены следующие фотографии:'
        display(HTML(text_for_student))

        for ind, _photo in enumerate(user_shuttle.memory):
            display(HTML(f"№{ind + 1}"))
            root_path = str(_photo.img_path).split('\\')[-1]
            colab_path = "diohod_bot/img/artifacts/" + root_path
            photo = render_photo(colab_path)
            display(photo)
    except:
        render_photo(None)

# img = open('diohod_bot/img/artifacts/dino.png', 'rb').read()
go(1, "move()\nrotate()\nphoto()")