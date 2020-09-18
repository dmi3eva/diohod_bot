import PySimpleGUI as sg
from ui.missions_menu import get_missions_menu
from planet.warehouse import planet_01
from utils import *

MAIN_WIDTH = 100
MAIN_HEIGHT = 500




def get_main_menu():
    missions_menu = get_missions_menu(MAIN_WIDTH * 2, MAIN_HEIGHT)
    task_label = sg.Text("Описание миссии:",
            size=(MAIN_WIDTH, 1),
            background_color='yellow',
            text_color='black',
            pad=(0, 0))
    mission_task = deEmojify(planet_01.mission.text)
    task_text = sg.Text(
            text=mission_task,
            key='MISSION_TEXT',
            size=(MAIN_WIDTH // 2, 10),
            background_color='white',
            text_color='black',
            pad=(0, 0))
    task_img = sg.Image(filename=planet_01.mission.ill_path, key='MISSION_IMG')
    work_zone = sg.Column(
        [
            [task_label],
            [task_text],
            [task_img]
        ],
        key='WORK_ZONE',
        visible=True,
        size=(MAIN_WIDTH * 4, MAIN_HEIGHT),
        scrollable=True
    )
    progr_label = sg.Text("Здесь вы можете писать инструкции диоходу:",
                         size=(MAIN_WIDTH, 1),
                         background_color='white',
                         text_color='black',
                         pad=(0, 0))
    snippet = sg.MLine(
            size=(MAIN_WIDTH // 2, 25),
            text_color='black',
            key='USER_CODE',
            pad=(0, 0))
    start_button = sg.Button(
        button_text="Запустить миссию!",
        key='START_MISSION',
        enable_events=True,
        pad=(0, 10)
    )
    progr_zone = sg.Column(
        [
            [progr_label],
            [snippet],
            [start_button]
        ],
        key='PROGR_ZONE',
        visible=True,
        size=(MAIN_WIDTH * 4, MAIN_HEIGHT),
        scrollable=True
    )
    layout = [[missions_menu, work_zone, progr_zone]]
    window = sg.Window(title="Пульт управления диоходом", layout=layout, margins=(1, 1))
    return window