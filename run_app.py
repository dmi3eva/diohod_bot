import PySimpleGUI as sg
from ui.main_window import get_main_menu
from ui.result_popup import get_popup_window
from planet.warehouse import *
from converter import *
from shuttle import Shuttle
from utils import *

sg.theme('LightGrey1')
window = get_main_menu()

BUTTON_MAPPING = {
    'MISSION_01': planet_01,
    'MISSION_02': planet_02,
    'MISSION_03': planet_03,
    'MISSION_04': planet_04,
    'MISSION_05': planet_05,
    'MISSION_06': planet_06,
    'MISSION_07': planet_07,
    'MISSION_08': planet_08,
    'MISSION_09': planet_09
}

current_planet = planet_01
while True:
    event, values = window.read()
    if event is None or event == 'EXIT':
        break
    for mission, planet in BUTTON_MAPPING.items():
        if event == mission:
            current_planet = planet
            mission_task = deEmojify(planet.mission.text)
            window['MISSION_TEXT'].update(mission_task)
            if planet.mission.ill_path is not None and os.path.exists(planet.mission.ill_path):
                window['MISSION_IMG'].update(visible=True)
                window['MISSION_IMG'].update(filename=planet.mission.ill_path)
            else:
                window['MISSION_IMG'].update(visible=False)
    if event == 'DIO_HELP':
        sg.popup(HELP_TEXT)
    if event == 'START_MISSION':
        text_for_student = ""
        img_for_student = []
        try:
            user_shuttle = Shuttle(current_planet)
            user_program = convert_to_lines(values['USER_CODE'])
            user_shuttle.execute(user_program)
            text_for_student = 'Диоход завершил свою миссию!\n'
            unique_amount = len(user_shuttle.explored_cells)
            text_for_student += 'Cфотографировано различных клеток планеты: {} шт.\n'.format(unique_amount)
            if len(user_shuttle.memory) == 0:
                text_for_student += 'Не было получено ни одной фотографии'
            else:
                text_for_student += 'Были получены следующие фотографии:'
            img_for_student = [_ph.img_path for _ph in user_shuttle.memory]
        except CompilationError as err:
            text_for_student = """Ошибка в коде программы:\n{}""".format(err.message)
        except ActionError as err:
            text_for_student = """Получено экстренное сообщение от диохода:\n{}""".format(err.message)
        except PlanetError as err:
            text_for_student = """{}""".format(err.message)
        except:
            text_for_student = "Ошибка в программе"
        popup_window = get_popup_window(text_for_student, img_for_student)
        popup_event, popup_values = popup_window.read(close=True)




window.close()