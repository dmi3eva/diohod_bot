from enum import Enum

class State(Enum):
    MENU = 0
    HELP = 1
    RESEARCH = 2
    NEWS = 3

class Controller:
    def __init__(self):
        self.current_state = {}