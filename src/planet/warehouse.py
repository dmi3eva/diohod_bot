from planet import *
from settings import *
from artifact.warehouse import *
from enums import *


# Планета №1
mission_01 = Mission(
    """На снимках с телескопа видно, что на этой планете располагается неопознанный объект.
    \n\U0001F4F8 Сфотографируйте его, добравшись до квадрата, помеченного знаком сюрприза.
    \n\U0001F4F0 Не забудьте опубликовать новость.
    \nОсторожно! Не свалитесь с планеты! Похоже, она плоская и имеет форму квадрата 5 на 5.
    \nПрограмму пишите прямо в сообщении.""",
    os.path.join(MISSIONS_IMG, 'planet_01.png')
)
planet_01 = Planet(width=5, height=5, base_x=1, base_y=0, shape=PlanetShape.SQUARE, mission=mission_01)
planet_01.area[2][1] = idol

# Планета №2
mission_02 = Mission(
    """Базу на планете №2 окружили летающие тарелки. Надо понять, какова угроза.
    \nИзвестно, что на каких-то из четырех соседних по стороне клеток находятся НЛО.
    \nВаша миссия - узнать, сколько их.""",
    os.path.join(MISSIONS_IMG, 'planet_02.png')
)
planet_02 = Planet(width=5, height=5, base_x=2, base_y=2, shape=PlanetShape.SQUARE, mission=mission_02)
planet_02.area[3][2] = ufo_01
planet_02.area[2][3] = ufo_02
planet_02.area[1][2] = ufo_03

# Планета №3
mission_03 = Mission(
    """На планете №3 на расстоянии ровно 777 клеток (прямо на краю света) находится объект, который в своей жизни искал каждый.
    \nУзнайте, что это, и не свалитесь с планеты. Опасно!""",
    os.path.join(MISSIONS_IMG, 'planet_03.png')
)
planet_03 = Planet(width=3, height=778, base_x=1, base_y=0, shape=PlanetShape.SQUARE, mission=mission_03)
planet_03.area[1][777] = key

# Планета №4
mission_04 = Mission(
    """Известно, что на планете №4 где-то в желтой зоне находится золотое месторождение.
    \nОпределите его координаты.
    \nПостарайтесь написать максимально короткую программу.""",
    os.path.join(MISSIONS_IMG, 'planet_04.png')
)
planet_04 = Planet(width=6, height=6, base_x=0, base_y=0, shape=PlanetShape.SQUARE, mission=mission_04)
planet_04.area[5][1] = gold

CALL_PLANET_CORRESPONDENCE = {
    'planet_01': planet_01,
    'planet_02': planet_02,
    'planet_03': planet_03,
    'planet_04': planet_04
}