from enum import Enum
from error import *
from settings import *
from planet import *
from artifact import *
from converter import *


class Compass(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


class ExecuteCode(Enum):
    ALL_RIGHT = 0


class Shuttle:
    def __init__(self, planet: Planet):
        self.__planet = planet
        self.direction = Compass.NORTH
        self.x = planet.base_x
        self.y = planet.base_y
        self.memory = []
        self.not_photographed = planet.get_all_objects_cells()
        self.unique_cells_amount = 0
        self.history = planet.get_area_scheme()
        self.time = 0

    def execute(self, lines):
        if 'repeat' in lines[0]:
            self.execute_cycle(lines)
        elif 'if' in lines[0]:
            self.execute_condition(lines)
        elif 'photo' in lines[0]:
            self.execute_photo(lines)
        elif 'rotate' in lines[0]:
            self.execute_rotate(lines)
        elif 'move' in lines[0]:
            self.execute_move(lines)
        elif 'pop' in lines[0]:
            self.execute_pop(lines)
        else:
            raise CompilationError('Команда ```\"{}\"``` не распознана'.format(lines[0]))

    def execute_cycle(self, lines):
        cycle = parse_cycle(lines)
        for _ in range(cycle.amount):
            self.execute(cycle.body)
        self.execute(cycle.remain)

    def execute_condition(self, lines):
        condition = parse_condition(lines)
        if len(self.memory) == 0:
            raise CompilationError('В памяти нет фото. Невозможно проверить условие!')
        last_photo = self.memory[-1]
        if last_photo.alias == condition.alias:
            self.execute(condition.true_block)
        else:
            self.execute(condition.false_block)
        self.execute(condition.remain)

    def execute_photo(self, lines):
        photo = parse_pop(lines)
        if len(self.memory) < MEMORY_LIMIT:
            self.memory.append(self._make_photo())
        if len(self.memory) == MEMORY_LIMIT:
            self.memory.append(camera_roll)
        self.execute(photo.remain)

    def execute_rotate(self, lines):
        rotate = parse_rotate(lines)
        self.direction = rotate.direction
        self.execute(rotate.remain)

    def execute_move(self, lines):
        move = parse_move(lines)
        photo = self._make_photo()
        if photo.alias == 'cosmos':
            raise ActionError("Связь с диоходом потеряна!")
        if photo.alias == 'dino':
            raise ActionError("Получено экстренное сообщение: \"На планете обнаружен диноза...\"")
        if photo.alias == 'volcano':
            raise ActionError("Получено экстренное сообщение: \"Зря я сюда пошёл: тут был вулкан. Прощайте!\"")
        _x, _y = self._get_coordinate()
        self.x = _x
        self.y = _y
        self.execute(move.remain)

    def execute_pop(self, lines):
        pop = parse_pop(lines)
        if len(self.memory) == 0:
            raise CompilationError('Не могу удалить фото - память пуста.')
        self.memory.pop()
        self.execute(pop.remain)

    def _make_photo(self):
        _x, _y = self._get_coordinate()
        if _x < 0 or _x >= self.__planet.width:
            return cosmos
        if _y < 0 or _y >= self.__planet.height:
            return cosmos
        if self.__planet.area[_x][_y] is None:
            return empty
        return self.__planet.area[_x][_y]

    def _get_coordinate(self):
        delta = {
            Compass.WEST: (-1, 0),
            Compass.EAST: (1, 0),
            Compass.NORTH: (0, 1),
            Compass.SOUTH: (0, -1)
        }
        _x = self.x + delta[self.direction][0]
        _y = self.x + delta[self.direction][0]
        if self.__planet.shape in [PlanetShape.TORUS, PlanetShape.X_CYLINDER]:
            _x %= self.__planet.width
        if self.__planet.shape in [PlanetShape.TORUS, PlanetShape.Y_CYLINDER]:
            _y %= self.__planet.width
        return _x, _y




from planet.warehouse import *
test_shuttle = Shuttle(planet_01)
test_commands_1 = ['repeat(3)', '{', 'a', 'repeat(2)', '{', 'b', '}', 'c', '}', 'd']
test_commands_2 = ['t', 'if last is volcano', '{', 'x', 'y', '} else', '{', 'z', '}', 'ostatok']
test_shuttle.execute(test_commands_2)