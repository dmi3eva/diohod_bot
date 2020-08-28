from enum import Enum
from enums import *

class Compass(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


class ExecuteCode(Enum):
    ALL_RIGHT = 0

class PlanetShape(Enum):
    SQUARE = 0
    TORUS = 1
    X_CYLINDER = 2  # замкнуто по оси ОХ
    Y_CYLINDER = 3  # замкнуто по оси ОУ