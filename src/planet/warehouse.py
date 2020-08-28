from planet import *
from settings import *
from artifact.warehouse import *


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


CALL_PLANET_CORRESPONDENCE = {
    'planet_01': planet_01
}