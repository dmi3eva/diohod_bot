from random import choice, randint

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
    """Базу на планете №2 окружили летающие тарелки. Надо понять, какова угроза?
    \n\U0001F6F8 Итак, известно, что на каких-то из четырех соседних по стороне клеток находятся НЛО.
    \n\U0001F3AF Ваша миссия - узнать, сколько их.""",
    os.path.join(MISSIONS_IMG, 'planet_02.png')
)
planet_02 = Planet(width=5, height=5, base_x=2, base_y=2, shape=PlanetShape.SQUARE, mission=mission_02)
planet_02.area[3][2] = ufo_01
planet_02.area[2][3] = ufo_02
planet_02.area[1][2] = ufo_03

# Планета №3
mission_03 = Mission(
    """На планете №3 на расстоянии ровно 777 клеток (прямо на краю света) находится объект, который в своей жизни искал каждый.
    \n\U0001F3AF Узнайте, что это, и не свалитесь с планеты. Опасно!""",
    os.path.join(MISSIONS_IMG, 'planet_03.png')
)
planet_03 = Planet(width=3, height=778, base_x=1, base_y=0, shape=PlanetShape.SQUARE, mission=mission_03)
planet_03.area[1][777] = key

# Планета №4
mission_04 = Mission(
    """Известно, что на планете №4 где-то в желтой зоне находится золотое месторождение.
    \n\U0001F3AF Определите его координаты, если база находится в точке (0, 0).
    \n\U0001F3AF Постарайтесь написать максимально короткую программу.""",
    os.path.join(MISSIONS_IMG, 'planet_04.png')
)
planet_04 = Planet(width=6, height=6, base_x=0, base_y=0, shape=PlanetShape.SQUARE, mission=mission_04)
planet_04.area[5][1] = gold


# Планета №5
mission_05 = Mission(
    text="""Планета №5 плоская, имеет размер 4 на 4 клеточки и базу в точке (0,0). Самое главное - по ней бродят животные!!!
    \n\U0001F3AF Обойдите всю планету и найдите всех!
    \n\U0001F43E Имейте в виду - животные медленно, но перемещаются. После каждого нового пуска диохода животные будут оказываться в новых местах.""",
    image=os.path.join(MISSIONS_IMG, 'planet_05.png')
)
planet_05 = Planet(width=4, height=4, base_x=0, base_y=0, shape=PlanetShape.SQUARE, mission=mission_05)
planet_05.area[randint(1, 3)][0] = mammoth
planet_05.area[1][0] = orangutan
planet_05.area[randint(1, 2)][2] = goose
planet_05.area[3][3] = unicorn


# Планета №6
mission_06 = Mission(
    """Давным-давно на планете №6 произошло крушение ракеты. Теперь на планете полно осколков.
    \n\U0001F3AF Попробуйте понять, как называлась разбившаяся ракета.
    \n\U0001F3E0 Координаты базы: (0, 0). Планета плоская и имеет форму квадрата 1 на 1000.
    \n\U0001F32A Имейте в виду - на планете дует сильный ветер и осколки перемещаются. 
    \n\U0001F4F7 Память фотоаппарата позволяет сохранить только 30 кадров."""
    # os.path.join(MISSIONS_IMG, 'planet_06.png')
)
planet_06 = Planet(width=1, height=1000, base_x=0, base_y=0, shape=PlanetShape.SQUARE, mission=mission_06)
planet_06.area[0][randint(1, 150)] = shard
planet_06.area[0][randint(151, 300)] = letter_e
planet_06.area[0][randint(301, 450)] = letter_l
planet_06.area[0][randint(451, 600)] = letter_o
planet_06.area[0][randint(601, 750)] = letter_p
planet_06.area[0][randint(751, 1000)] = letter_t

# Планета №7
mission_07 = Mission(
    """По снимкам из космоса видно, что на планете №7 где-то на одной вертикали с базой (к северу от неё) находится неопознанный монументальный объект.
    \n\U0001F3AF Попробуйте опознать его.
    \n\U0001F409 Внимание! По этой же вертикали бегает динозавр. Встречи с ним диоход не переживет.
    \n\U0001F3E0 Размер планеты: 3 на 100. База находится  в точке (1, 0).""",
    os.path.join(MISSIONS_IMG, 'planet_07.png')
)
planet_07 = Planet(width=3, height=100, base_x=1, base_y=0, shape=PlanetShape.SQUARE, mission=mission_07)
planet_07.area[1][randint(1, 75)] = dino
planet_07.area[1][84] = lenin

# Планета №8
mission_08 = Mission(
    """В зоне по периметру планеты №8 располагается некий огромный объект.
    \n\U0001F3AF Определите, что это?
    \n\U0001F409 По зеленой зоне бегает динозавр. Встреться с ним не хотелось бы (мягко говоря).
    \n\U0001F3E0 Размер планеты: 5 на 5. База находится в точке (2, 2).""",
    os.path.join(MISSIONS_IMG, 'planet_08.png')
)
planet_08 = Planet(width=5, height=5, base_x=2, base_y=2, shape=PlanetShape.SQUARE, mission=mission_08)
dino_coord = choice([(2, 3), (2, 1), (3, 2), (1, 2)])
planet_08.area[dino_coord[0]][dino_coord[1]] = dino
planet_08.area[0][1] = pyramid

# Планета №9
mission_09 = Mission(
    """Самая далекая и самая интересная планета. Про нее неизвестно НИЧЕГО. Исследуйте её. Подробно опишите результаты и свои гипотезы."""
)
planet_09 = Planet(width=3, height=4, base_x=1, base_y=0, shape=PlanetShape.Y_CYLINDER, mission=mission_09)
planet_09.area[2][0] = volcano
planet_09.area[0][1] = volcano
planet_09.area[1][3] = volcano
planet_09.area[2][3] = volcano


CALL_PLANET_CORRESPONDENCE = {
    'planet_01': planet_01,
    'planet_02': planet_02,
    'planet_03': planet_03,
    'planet_04': planet_04,
    'planet_05': planet_05,
    'planet_06': planet_06,
    'planet_07': planet_07,
    'planet_08': planet_08,
    'planet_09': planet_09
}