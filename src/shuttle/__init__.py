try:
    from src.error import *
    from src.settings import *
    from src.planet import *
    from src.converter import *
    from src.enums import *
except:
    from diohod_bot.src.error import *
    from diohod_bot.src.settings import *
    from diohod_bot.src.planet import *
    from diohod_bot.src.converter import *
    from diohod_bot.src.enums import *

class Shuttle:
    def __init__(self, planet: Planet):
        self.__planet = planet
        self.direction = Compass.NORTH
        self.x = planet.base_x
        self.y = planet.base_y
        self.memory = []
        self.explored_cells = set()
        self.not_photographed = planet.get_all_objects_cells()
        self.history = planet.get_area_scheme()
        self.history[self.x][self.y].append(0)
        self.time = 0

    def execute(self, lines):
        if len(lines) > 0:
            if self.time > TIME_LIMIT:
                raise ActionError("\"Я слишком долго на этой планете - села батарея. Прощайте!\"")
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
        photo = parse_photo(lines)
        if len(self.memory) < MEMORY_LIMIT:
            _x, _y = self._get_coordinate()
            photography = self._make_photo(_x, _y)
            if photography.alias not in ['cosmos']:
                self.explored_cells.add((_x, _y))
            self.memory.append(photography)
            if (_x, _y) in self.not_photographed:
                self.not_photographed.remove((_x, _y))
        if len(self.memory) == MEMORY_LIMIT:
            self.memory.append(camera_roll)
        self.time += 1
        self.execute(photo.remain)

    def execute_rotate(self, lines):
        rotate = parse_rotate(lines)
        if rotate.direction is not None:
            self.direction = rotate.direction
        else:
            self.direction = {
                Compass.NORTH: Compass.EAST,
                Compass.WEST: Compass.NORTH,
                Compass.EAST: Compass.SOUTH,
                Compass.SOUTH: Compass.WEST
            }[self.direction]
        self.time += 1
        self.execute(rotate.remain)

    def execute_move(self, lines):
        move = parse_move(lines)
        _x, _y = self._get_coordinate()
        photo = self._make_photo(_x, _y)
        if photo.alias == 'cosmos':
            raise PlanetError("Связь с диоходом потеряна!")
        if photo.alias == 'dino':
            raise ActionError("\"На планете обнаружен диноза...\"")
        if photo.alias == 'volcano':
            raise ActionError("\"Зря я сюда пошёл: тут был вулкан. Прощайте!\"")
        self.x = _x
        self.y = _y
        self.time += 1
        self.history[_x][_y].append(self.time)
        self.execute(move.remain)

    def execute_pop(self, lines):
        pop = parse_pop(lines)
        if len(self.memory) == 0:
            raise CompilationError('Не могу удалить фото - память пуста.')
        self.memory.pop()
        if len(self.memory) == MEMORY_LIMIT:
            self.memory.pop()
        self.time += 1
        self.execute(pop.remain)

    def _make_photo(self, x_coord, y_coord):
        if x_coord < 0 or x_coord >= self.__planet.width:
            return cosmos
        if y_coord < 0 or y_coord >= self.__planet.height:
            return cosmos
        if self.__planet.area[x_coord][y_coord] is None:
            return empty
        self.time += 1
        return self.__planet.area[x_coord][y_coord]

    def _get_coordinate(self):
        delta = {
            Compass.WEST: (-1, 0),
            Compass.EAST: (1, 0),
            Compass.NORTH: (0, 1),
            Compass.SOUTH: (0, -1)
        }
        _x = self.x + delta[self.direction][0]
        _y = self.y + delta[self.direction][1]
        if self.__planet.shape in [PlanetShape.TORUS, PlanetShape.X_CYLINDER]:
            _x %= self.__planet.width
        if self.__planet.shape in [PlanetShape.TORUS, PlanetShape.Y_CYLINDER]:
            _y %= self.__planet.height
        return _x, _y