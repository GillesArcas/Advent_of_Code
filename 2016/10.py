"""
--- 2016 --- Day 10: Balance Bots ---
"""


import re
from collections import defaultdict


EXAMPLES1 = (
    ('10-exemple1.txt', None),
)

EXAMPLES2 = (
)

INPUT = '10.txt'


PAT1 = r'value (\d+) goes to (bot \d+)'
PAT2 = r'(bot \d+) gives low to ((?:bot|output) \d+) and high to ((?:bot|output) \d+)'


def give(dest, botvalues, outvalues, value):
    if dest.startswith('bot'):
        botvalues[dest].append(value)
        botvalues[dest].sort()
    else:
        outvalues[dest].append(value)


def read_data(filename):
    with open(filename) as f:
        lines = f.readlines()

    botvalues = defaultdict(list)
    outvalues = defaultdict(list)
    actions = {}

    for line in lines:
        if match := re.match(PAT1, line):
            value, bot = match.group(1, 2)
            give(bot, botvalues, outvalues, int(value))

        elif match := re.match(PAT2, line):
            bot, destlow, desthigh = match.group(1, 2, 3)
            actions[bot] = (destlow, desthigh)

        else:
            assert 0, line

    return botvalues, outvalues, actions


def code1(data):
    botvalues, outvalues, actions = data

    while actions:
        for bot, action in actions.items():
            if len(botvalues[bot]) == 2:
                break
        else:
            continue
        del actions[bot]
        give(action[0], botvalues, outvalues, botvalues[bot][0])
        give(action[1], botvalues, outvalues, botvalues[bot][1])

        if botvalues[bot][0] == 17 and botvalues[bot][1] == 61:
            return bot

    return None


def code2(data):
    botvalues, outvalues, actions = data

    while actions:
        for bot, action in actions.items():
            if len(botvalues[bot]) == 2:
                break
        else:
            continue
        del actions[bot]
        give(action[0], botvalues, outvalues, botvalues[bot][0])
        give(action[1], botvalues, outvalues, botvalues[bot][1])

    return outvalues['output 0'][0] * outvalues['output 1'][0] * outvalues['output 2'][0]


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
