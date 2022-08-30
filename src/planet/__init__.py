from enums import *
from artifact.warehouse import *


class Mission():
    def __init__(self, text=None, image=None):
        self.text = text
        self.ill_path = image

    def get_illustration(self):
        if self.ill_path is None:
            return None
        if os.path.exists(self.ill_path):
            return open(self.ill_path, 'rb')
        return None


class Planet:
    def __init__(self, width=6, height=7, base_x=0, base_y=0, shape=PlanetShape.SQUARE, mission=Mission()):
        # base_x - то номер столбцы
        self.mission = mission
        self.area = [[None for _ in range(height)] for _ in range(width)]
        self.width = width
        self.height = height
        self.shape = shape

        self.area[base_x][base_y] = base
        self.base_x = base_x
        self.base_y = base_y

    def get_area_scheme(self):
        area_scheme = [[[] for _ in range(self.height)] for _ in range(self.width)]
        for i, _line in enumerate(self.area):
            for j, _cell in enumerate(_line):
                if _cell is None:
                    content = []
                else:
                    content = ['({})'.format(_cell.description[0])]
                area_scheme[i][j] = content
        return area_scheme

    def get_all_objects_cells(self):
        all_objects = []
        for i, _line in enumerate(self.area):
            for j, _cell in enumerate(_line):
                if _cell is not None:
                    all_objects.append((i, j))
        return all_objects