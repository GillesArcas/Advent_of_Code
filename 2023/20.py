"""
--- Day 20: Pulse Propagation ---
"""


import re
import math
from itertools import pairwise


EXAMPLES1 = (
    ('20-exemple1.txt', 32000000),
    ('20-exemple2.txt', 11687500),
)

EXAMPLES2 = (
)

INPUT = '20.txt'


def read_data(filename):
    with open(filename) as f:
        lines = f.readlines()
    modules = {}
    modules['button'] = dict(type='button', dest=['broadcaster'])
    for line in lines:
        match = re.match('([%&]?)([a-z]+) -> (.*)', line.strip())
        modules[match[2]] = {'type': match[1], 'dest': match[3].split(', ')}
        if match[1] == '':
            assert match[2] == 'broadcaster'
            modules[match[2]]['type'] = 'broadcast'
        elif match[1] == '%':
            modules[match[2]]['state'] = 'off'
        elif match[1] == '&':
            modules[match[2]]['input'] = {}

    missing = []
    for module in modules:
        for dest in modules[module]['dest']:
            if dest not in modules:
                missing.append(dest)
    for module in missing:
        modules[module] = {'type': None, 'dest': []}

    for module in modules:
        for dest in modules[module]['dest']:
            if modules[dest]['type'] == '&':
                modules[dest]['input'][module] = 'low'

    return modules


def code1(modules):
    fifo = []
    count = {'low': 0, 'high': 0}
    for _ in range(1000):
        fifo.append(('button', 'broadcaster', 'low'))  # event = (origin, destination, pulse)
        count['low'] += 1
        while fifo:
            origin, module, pulse = fifo.pop(0)

            if modules[module]['type'] == 'broadcast':
                for dest in modules[module]['dest']:
                    fifo.append((module, dest, pulse))
                    count[pulse] += 1

            if modules[module]['type'] == '%':
                if pulse == 'high':
                    pass
                else:
                    modules[module]['state'] = {'off': 'on', 'on': 'off'}[modules[module]['state']]
                    pulse = 'low' if (modules[module]['state'] == 'off') else 'high'
                    for dest in modules[module]['dest']:
                        fifo.append((module, dest, pulse))
                        count[pulse] += 1

            if modules[module]['type'] == '&':
                modules[module]['input'][origin] = pulse
                pulse = 'low' if all(_ == 'high' for _ in modules[module]['input'].values()) else 'high'
                for dest in modules[module]['dest']:
                    fifo.append((module, dest, pulse))
                    count[pulse] += 1

    print(count)
    return count['low'] * count['high']


def code2(modules):
    values = {'nd': [], 'pc': [], 'vd': [], 'tx': []}
    fifo = []
    for press in range(1, 20_000):
        fifo.append(('button', 'broadcaster', 'low'))  # event = (origin, destination, pulse)
        while fifo:
            origin, module, pulse = fifo.pop(0)
            if pulse == 'low' and module in values:
                values[module].append(press)

            if modules[module]['type'] == 'broadcast':
                for dest in modules[module]['dest']:
                    fifo.append((module, dest, pulse))

            if modules[module]['type'] == '%':
                if pulse == 'high':
                    pass
                else:
                    modules[module]['state'] = {'off': 'on', 'on': 'off'}[modules[module]['state']]
                    pulse = 'low' if (modules[module]['state'] == 'off') else 'high'
                    for dest in modules[module]['dest']:
                        fifo.append((module, dest, pulse))

            if modules[module]['type'] == '&':
                modules[module]['input'][origin] = pulse
                pulse = 'low' if all(_ == 'high' for _ in modules[module]['input'].values()) else 'high'
                for dest in modules[module]['dest']:
                    fifo.append((module, dest, pulse))

    # check visually that each predecessor of rx emits a low pulse with a period
    # equal to the first time it emits a low pulse
    for module, vals in values.items():
        print('--', module)
        print('first', vals[0])
        for x, y in pairwise(vals[1:]):
            print('delta', y - x)

    return math.lcm(*[_[0] for _ in values.values()])


def test(n, code, examples, myinput):
    for fn, expected in examples:
        print(fn)
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
