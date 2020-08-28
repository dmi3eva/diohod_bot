import re
from error import *

from settings import *
from enums import *



def preprocess_line(command):
    """Предобработка команды"""
    command = command.lower()
    command = command.strip()
    while ' ' in command:
        command = command.replace('  ', ' ')
    return command


def preprocess_block(block):
    command = block.replace('\t', '\n')
    while '\n\n' in command:
        command = command.replace('\n\n', '\n')
    return block


def extract_block(lines):
    """Возвращает самый крупный первый блок"""
    text = '#'.join(lines)
    brackets_stack = []
    for _ind, _symbol in enumerate(text):
        if _symbol == '{':
            brackets_stack.append(_ind)
        if _symbol == '}':
            if len(brackets_stack) == 0:
                raise CompilationError('Проверьте, правильно ли вы расставили скобки?')
            if len(brackets_stack) == 1:
                block = text[brackets_stack.pop() + 1:_ind - 1].split('#')
                remain = text[_ind + 1:].split('#')
                return [_l for _l in block if len(_l) > 0], [_l for _l in remain if len(_l) > 0]
            brackets_stack.pop()
    raise CompilationError('Проверьте, правильно ли вы расставили скобки?')


def convert_to_lines(user_program):
    user_program = preprocess_block(user_program)
    send_commands = re.findall('send', user_program)
    if len(send_commands) > 1:
        raise CompilationError('Каждый диоход может послать фото только 1 раз.')
    lines = user_program.split('\n')
    lines = [preprocess_line(_l) for _l in lines]
    return lines


class Cycle:
    def __init__(self, amount, body, remain):
        self.amount = amount
        self.body = body
        self.remain = remain


def parse_cycle(lines):
    hat = lines[0].replace(' ', '').strip()
    validation = re.findall(CYCLE_HAT_PATTERN, hat)
    if len(validation) != 1 or validation[0] != hat:
        raise CompilationError('Проблема в строке ```\"{}\"```'.format(hat))
    amount = int(hat[hat.index('(') + 1:hat.index(')')])
    body, remain = extract_block(lines)
    return Cycle(amount, body, remain)


class Condition:
    def __init__(self, object_alias, true_block, false_block, remain):
        self.alias = object_alias
        self.true_block = true_block
        self.false_block = false_block
        self.remain = remain


def parse_condition(lines):
    alias, true_block, remain = _parse_true_block(lines)
    false_block, remain = _parse_false_block(remain)
    return Condition(alias, true_block, false_block, remain)


def _parse_true_block(lines):
    hat = lines[0].strip()
    validation = re.findall(STATEMENT_HAT_PATTERN, hat)
    if len(validation) != 1 or validation[0] != hat:
        raise CompilationError('Проблема в строке ```\"{}\"```'.format(hat))
    alias = hat[hat.index('is ') + 3:]
    if alias[-1] == '\{':
        alias = alias[:-1]
    alias = alias.strip()
    true_block, remain = extract_block(lines)
    return alias, true_block, remain


def _parse_false_block(lines):
    hat = lines[0].strip()
    validation = re.findall(ELSE_HAT_PATTERN, hat)
    if len(validation) != 1 or validation[0] != hat:
        raise CompilationError('Проблема в строке ```\"{}\"```'.format(hat))
    false_block, remain = extract_block(lines)
    return false_block, remain


class Pop:
    def __init__(self, remain):
        self.remain = remain


def parse_pop(lines):
    hat = lines[0].replace(' ', '').strip()
    if hat != 'pop()':
        raise CompilationError('Проблема в строке ```\"{}\"```'.format(hat))
    return Pop(lines[1:])


class Photo:
    def __init__(self, remain):
        self.remain = remain


def parse_photo(lines):
    hat = lines[0].replace(' ', '').strip()
    if hat != 'photo()':
        raise CompilationError('Проблема в строке ```\"{}\"```'.format(hat))
    return Photo(lines[1:])


class Move:
    def __init__(self, remain):
        self.remain = remain


def parse_move(lines):
    hat = lines[0].replace(' ', '').strip()
    if hat != 'move()':
        raise CompilationError('Проблема в строке ```\"{}\"```'.format(hat))
    return Move(lines[1:])


class Rotate:
    def __init__(self, direction, remain):
        self.direction = direction
        self.remain = remain


def parse_rotate(lines):
    hat = lines[0].replace(' ', '').strip().lower()
    validation = re.findall(ROTATE_HAT_PATTERN, hat)
    if (len(validation) != 1 or validation[0] != hat) and (''.join(validation[0]) != hat):
        raise CompilationError('Проблема в строке ```\"{}\"```'.format(hat))
    direction_text = hat[hat.index('(') + 1:hat.index(')')]

    direction = {
        'north': Compass.NORTH,
        'west': Compass.WEST,
        'east': Compass.EAST,
        'south': Compass.SOUTH,
        '': None
    }[direction_text]
    return Rotate(direction, lines[1:])