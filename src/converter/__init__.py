import re
from error import *

from settings import *


def preprocess_line(command):
    """Предобработка команды"""
    command = command.lower()
    command = command.strip()
    while ' ' in command:
        command = command.replace('  ', ' ')
    return command


def preprocess_block(block):
    block = block.replace('\t', '\n')
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
                raise ShuttleError('Проверьте, правильно ли вы расставили скобки?')
            if len(brackets_stack) == 1:
                block = text[brackets_stack.pop() + 1:_ind - 1].split('#')
                remain = text[_ind + 1:].split('#')
                return [_l for _l in block if len(_l) > 0], [_l for _l in remain if len(_l) > 0]
            brackets_stack.pop()
    raise ShuttleError('Проверьте, правильно ли вы расставили скобки?')


def convert_to_lines(user_program):
    user_program = preprocess_block(user_program)
    send_commands = re.findall('send', user_program)
    if len(send_commands) > 1:
        raise ShuttleError('Каждый диоход может послать фото только 1 раз.')
    lines = user_program.split('\n')
    lines = [preprocess_line(_l) for _l in lines]
    return lines


class Cycle:
    def __init__(self, amount, body, remain):
        self.amount = amount
        self.body = body
        self.remain = remain


def parse_cycle(lines):
    hat = lines[0].replace(' ', '')
    validation = re.findall(CYCLE_HAT_PATTERN, hat)
    if len(validation) != 1 or validation[0] != hat:
        raise ShuttleError('Проблема в строке ```\"{}\"```'.format(hat))
    amount = int(hat[hat.index('(') + 1:hat.index(')')])
    body, remain = extract_block(lines)
    return Cycle(amount, body, remain)


class Condition:
    def __init__(self, sensor, artifact, true_block, false_block, remain):
        self.amount = sensor
        self.body = artifact
        self.true_block = true_block
        self.false_block = false_block
        self.remain = remain


def parse_condition(lines):
    hat = lines[0].replace(' ', '')
    validation = re.findall(CYCLE_HAT_PATTERN, hat)
    if len(validation) != 1 or validation[0] != hat:
        raise ShuttleError('Проблема в строке ```\"{}\"```'.format(hat))
    amount = int(hat[hat.index('(') + 1:hat.index(')')])
    body, remain = extract_block(lines)
    return Cycle(amount, body, remain)