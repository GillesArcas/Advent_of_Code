"""
--- Day 15: Lens Library ---
"""


import re


EXAMPLES1 = (
    ('15-exemple1.txt', 1320),
)

EXAMPLES2 = (
    ('15-exemple1.txt', 145),
)

INPUT = '15.txt'


def read_data(filename):
    with open(filename) as f:
        return f.readline().strip().split(',')


def hashcode(s):
    hashc = 0
    for char in s:
        hashc = ((hashc + ord(char)) * 17) % 256
    return hashc


def code1(steps):
    return sum(hashcode(step) for step in steps)


def code2(steps):
    boxes = [[] for _ in range(256)]
    for step in steps:
        label, op, foclen = re.match(r'(\w+)(-|=)(\d*)', step).groups()
        h = hashcode(label)
        box = boxes[h]
        index = -1
        for i, lens in enumerate(box):
            if lens[0] == label:
                index = i
                break

        if op == '-':
            if index >= 0:
                del box[index]
        elif op == '=':
            if index < 0:
                box.append([label, foclen])
            else:
                box[index][1] = foclen

    focuspower = 0
    for ibox, box in enumerate(boxes, 1):
        for ilens, lens in enumerate(box, 1):
            focuspower += ibox * ilens * int(lens[1])

    return focuspower



def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
