from enum import Enum

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
        self.time = 0

    def execute(self, lines):
        if 'repeat' in lines[0]:
            self.execute_cycle(lines)
        elif 'if' in lines[0]:
            self.execute_condiotion(lines)
        else:
            print(lines[0])
            if len(lines) > 1:
                self.execute(lines[1:])

    def execute_cycle(self, lines):
        cycle = parse_cycle(lines)
        for _ in range(cycle.amount):
            self.execute(cycle.body)
        self.execute(cycle.remain)

    def execute_condition(self, lines):
        condition = parse_condition(lines)
        for _ in range(cycle.amount):
            self.execute(cycle.body)
        self.execute(cycle.remain)


test_shuttle = Shuttle(Planet())
test_commands = ['repeat(3)', '{', 'a', 'repeat(2)', '{', 'b', '}', 'c', '}', 'd']
test_shuttle.execute(test_commands)


