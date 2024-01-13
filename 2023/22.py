"""
--- Day 22: Sand Slabs ---
"""


import re
import copy
from itertools import product


EXAMPLES1 = (
    ('22-exemple1.txt', 5),
)

EXAMPLES2 = (
    ('22-exemple1.txt', None),
)

INPUT = '22.txt'


def read_data(filename):
    with open(filename) as f:
        text = f.read()

    data = re.findall(r'(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)', text)
    bricks = [[index] + [int(_) for _ in brick] for index, brick in enumerate(data)]
    return bricks


def set_list(mylist, index, val, default):
    """
    set `mylist[index] = val` making sure `mylist[index]` exists
    """
    if index >= len(mylist):
        mylist += [default] * (index - len(mylist) + 1)
        assert len(mylist) == index + 1, (mylist, index)
    assert mylist[index] is None
    mylist[index] = val


def xy(x1, y1, x2, y2):
    return product(range(x1, x2 + 1), range(y1, y2 + 1))


def snapshot(bricks):
    stack = {}
    for index, x1, y1, z1, x2, y2, z2 in reversed(bricks):
        for x, y in xy(x1, y1, x2, y2):
            stack[x, y] = []

    for index, x1, y1, z1, x2, y2, z2 in reversed(bricks):
        for x, y in xy(x1, y1, x2, y2):
            for z in range(z1, z2 + 1):
                set_list(stack[x, y], z, index, default=None)

    # ensure above all bricks may be tested
    for zlist in stack.values():
        zlist.append(None)

    return stack


def settle(bricks, stack):
    """
    Return number of lowered bricks
    """
    changed_bricks = set()
    changed = True
    while changed:
        changed = False
        for brick in reversed(bricks):
            index, x1, y1, z1, x2, y2, z2 = brick
            if z1 > 1 and all(stack[x, y][z1 - 1] is None for x, y in xy(x1, y1, x2, y2)):
                # print('lower', brick)
                brick[3] -= 1
                brick[6] -= 1
                for x, y in xy(x1, y1, x2, y2):
                    stack[x, y][z1 - 1] = index
                    stack[x, y][z2] = None
                changed_bricks.add(index)
                changed = True
    return len(changed_bricks)


def bricks_above(index, bricks, stack):
    _, x1, y1, _, x2, y2, z2 = bricks[index]
    above = {stack[x, y][z2 + 1 ]for x, y in xy(x1, y1, x2, y2)}
    if None in above:
        above.remove(None)
    return above


def bricks_below(index, bricks, stack):
    _, x1, y1, z1, x2, y2, _ = bricks[index]
    below = {stack[x, y][z1 - 1 ]for x, y in xy(x1, y1, x2, y2)}
    if None in below:
        below.remove(None)
    return below


def is_safe(index, bricks, stack):
    above = bricks_above(index, bricks, stack)
    return all(len(bricks_below(ibrick, bricks, stack)) > 1 for ibrick in above)


def code1(bricks):
    stack = snapshot(bricks)
    settle(bricks, stack)
    return sum(is_safe(brick[0], bricks, stack) for brick in bricks)


def code2(bricks):
    stack = snapshot(bricks)
    settle(bricks, stack)
    count = 0
    for brick in bricks:
        if is_safe(brick[0], bricks, stack) is False:
            stack2 = copy.deepcopy(stack)
            bricks2 = copy.deepcopy(bricks)
            index, x1, y1, z1, x2, y2, z2 = brick
            del bricks2[index]
            for x, y in xy(x1, y1, x2, y2):
                for z in range(z1, z2 + 1):
                    stack2[x, y][z] = None
            n = settle(bricks2, stack2)
            count += n
    return count


def test(n, code, examples, myinput):
    for fn, expected in examples:
        print(fn)
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
