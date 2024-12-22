"""
--- Day 14: Restroom Redoubt ---
"""


import re
import copy
from PIL import Image


EXAMPLES1 = (
    ('14-exemple1.txt', 12),
)

EXAMPLES2 = (
)

INPUT = '14.txt'


def read_data(filename):
    with open(filename) as f:
        text = f.read()
    match = re.match(r'size=(\d+),(\d+)', text)
    w, h = [int(_) for _ in match.groups()]
    robots = []
    for match in re.findall(r'p=(\d+),(\d+) v=(-?\d+),(-?\d+)', text):
        robots.append([int(_) for _ in match])
    return w, h, robots


def code1(data):
    w, h, robots = data
    seconds = 100
    array = [[0 for _ in range(w)] for _ in range(h)]
    for px, py, _, _ in robots:
        array[py][px] += 1
    for s in range(seconds):
        for robot in robots:
            px, py, vx, vy = robot
            array[py][px] -= 1
            px = (px + vx) % w
            py = (py + vy) % h
            array[py][px] += 1
            robot[0] = px
            robot[1] = py
    for line in array:
        print(''.join([str(_) for _ in line]))
    q1 = sum(sum(line[:w // 2]) for line in array[:h // 2])
    q2 = sum(sum(line[w // 2 + 1:]) for line in array[:h // 2])
    q3 = sum(sum(array[y][:w // 2]) for y in range(h // 2 + 1, h))
    q4 = sum(sum(array[y][w // 2 + 1:]) for y in range(h // 2 + 1, h))
    return q1 * q2 * q3 * q4


def period(robot, w, h):
    px0, py0, vx, vy = robot
    px = px0
    py = py0
    n = 0
    while 1:
        px2 = (px + vx) % w
        py2 = (py + vy) % h
        n += 1
        if px2 == px0 and py2 == py0:
            return n
        else:
            px = px2
            py = py2


def testperiod(w, h, robots):
    periods = [period(robot, w, h) for robot in robots]
    assert all(n == 10403 for n in periods)


def code2(data):
    """
    First, find the period of the process. There is no simple criteria to find
    the xmas tree in one area, so generate all images and search by eye.
    """
    w, h, robots = data
    array = [[0 for _ in range(w)] for _ in range(h)]
    for px, py, _, _ in robots:
        array[py][px] += 1
    array0 = copy.deepcopy(array)
    for s in range(1, 10403 + 1):
        print(s)
        for robot in robots:
            px, py, vx, vy = robot
            array[py][px] -= 1
            px = (px + vx) % w
            py = (py + vy) % h
            array[py][px] += 1
            robot[0] = px
            robot[1] = py

        img = Image.new( 'RGB', (w,h), "black")
        for i, line in enumerate(array):
            for j, pix in enumerate(line):
                if pix > 0:
                    img.putpixel((j,i), (255,255,255))
        img.save('c:/volatil/test' + str(s) + '.bmp')

    return None 


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
