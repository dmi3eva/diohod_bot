import os
import random
from enum import Enum

from settings import *
from artifact import *
from artifact.warehouse import *


class PlanetShape(Enum):
    SQUARE = 0
    TORUS = 1
    X_CYLINDER = 2
    Y_CYLYNDER = 3


class Mission():
    def __init__(self, text=None, image=None):
        self.text = text
        self.ill_path = image

    def get_illustration(self):
        if os.path.exists(self.ill_path):
            return open(self.ill_path, 'rb')
        return None


class Planet:
    def __init__(self, width=6, height=7, base_x=0, base_y=0, shape=PlanetShape.SQUARE, mission=Mission()):
        self.mission = mission
        self.area = [[dict() for _ in range(height)] for _ in range(width)]
        self.width = width
        self.height = height
        self.shape = shape

        for i in range(width):
            for j in range(height):
                self.area[i][j] = []

        self.area[base_x][base_y] = [base]
        self.base_x = base_x
        self.base_y = base_y
