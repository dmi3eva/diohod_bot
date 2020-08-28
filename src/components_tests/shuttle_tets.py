from shuttle import *
from planet.warehouse import *

test_shuttle = Shuttle(planet_01)
test_commands_1 = ['repeat(3)', '{', 'a', 'repeat(2)', '{', 'b', '}', 'c', '}', 'd']
test_commands_2 = ['t', 'if last is volcano', '{', 'x', 'y', '} else', '{', 'z', '}', 'ostatok']
test_commands_3 = ['move()', 'rotate(east)', 'photo']
test_commands_4 = ['move()', 'rotate(east)', 'photo()']
test_commands_5 = ['repeat(1000)', '{', 'move()', '}', 'photo()']
test_commands_6 = ['repeat(500)', '{', 'photo()', '}', 'photo()']
test_commands_7 = ['repeat(2000)', '{', 'photo()', '}', 'photo()']
test_commands_8 = ['repeat(20)', '{', 'move()', '}', 'photo()']
test_commands_9 = ['repeat(2000)', '{', 'move()', '}', 'photo()']
test_commands_10 = ['move()', 'rotate(east)', 'photo()', 'if last is idol', '{', 'rotate(south)', '}', 'else', '{', 'rotate(west)', '}']
test_commands_11 = ['move()', 'rotate(east)', 'photo()', 'if last is mumuka', '{', 'rotate(south)', '}', 'else', '{', 'rotate(west)', '}']
test_shuttle.execute(test_commands_11)
a = 7