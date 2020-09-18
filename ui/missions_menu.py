import PySimpleGUI as sg


def get_menu_item_label(label, width, key=None, tooltip=None, text_color='black'):
    return [sg.Text(label,
                    key=key,
                    enable_events=key is not None,
                    tooltip=tooltip,
                    size=(width, 2),
                    background_color='grey',
                    text_color=text_color,
                    pad=(0, 0))]

def get_menu_item(label, width, key=None):
    return [sg.Button(button_text=label,
                    key=key,
                    enable_events=key is not None,
                    size=(width // 8, 2),
                    pad=(0, 0))]


def get_missions_menu(width, height):
    missions_menu = sg.Column([
            get_menu_item('Миссия 1', width, 'MISSION_01'),
            get_menu_item('Миссия 2', width, 'MISSION_02'),
            get_menu_item('Миссия 3', width, 'MISSION_03'),
            get_menu_item('Миссия 4', width, 'MISSION_04'),
            get_menu_item('Миссия 5', width, 'MISSION_05'),
            get_menu_item('Миссия 6', width, 'MISSION_06'),
            get_menu_item('Миссия 7', width, 'MISSION_07'),
            get_menu_item('Миссия 8', width, 'MISSION_08'),
            get_menu_item('Миссия 9', width, 'MISSION_09'),
            get_menu_item('Справка', width, 'DIO_HELP')
        ],
        background_color='white',
        key='LEFT_MENU',
        size=(width, height),
        scrollable=True,
        vertical_scroll_only=True
    )

    return missions_menu