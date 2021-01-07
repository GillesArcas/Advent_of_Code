import os
from collections import defaultdict
import intcode


DATA = '13.txt'


def coordinates(tiles, target):
    for y, row in enumerate(tiles.values()):
        for x, tile in enumerate(row.values()):
            if tile == target:
                return x, y
    assert False, ('target not found', target)


def show_game(tiles):
    tilechar = {0: '.', 1: '#', 2: '¤', 3:'_', 4:'O'}
    for row in tiles.values():
        print(''.join(tilechar[tile] for tile in row.values()))


def draw_tiles(tiles, computer, inval, trace):
    while True:
        computer.run(inval, return_output=True)
        if computer.returned_on == 'terminate':
            break

        xpos = computer.outvalues[-1]
        computer.run([], return_output=True)
        ypos = computer.outvalues[-1]
        computer.run([], return_output=True)
        tileid = computer.outvalues[-1]

        if xpos == -1 and ypos == 0:
            score = tileid
            print('Score', score)
            show_game(tiles)
        else:
            tiles[ypos][xpos] = tileid
            if trace:
                print(xpos, ypos, tileid)
                show_game(tiles)

    return tiles


def play(tiles, computer, inval, trace):

    def callback():
        paddle_x, _ = coordinates(tiles, target=3)
        ball_x, _ = coordinates(tiles, target=4)
        if paddle_x < ball_x:
            return 1
        elif paddle_x > ball_x:
            return -1
        else:
            return 0

    while True:
        computer.run(inval, input_callback=callback, return_output=True)
        inval = []
        if computer.returned_on == 'terminate':
            break

        xpos = computer.outvalues[-1]
        computer.run([], return_output=True)
        ypos = computer.outvalues[-1]
        computer.run([], return_output=True)
        tileid = computer.outvalues[-1]

        if xpos == -1 and ypos == 0:
            score = tileid
            os.system('cls')
            print('Score', score)
            show_game(tiles)
        else:
            tiles[ypos][xpos] = tileid

    return tiles


def code1():
    with open(DATA) as f:
        strcode = f.readline().strip()
        code = intcode.parse_data(strcode)
    computer = intcode.Intcode(code)
    computer.verbose_output = False

    tiles = defaultdict(lambda: defaultdict(int))
    tiles = draw_tiles(tiles, computer, [], trace=False)

    n = 0
    for row in tiles.values():
        n += sum(tile == 2 for tile in row.values())

    show_game(tiles)
    print('1>', n)
    return tiles, computer


def code2():
    with open(DATA) as f:
        strcode = f.readline().strip()
        code = intcode.parse_data(strcode)
    computer = intcode.Intcode(code)
    computer.verbose_output = False
    computer.code[0] = 2

    tiles = defaultdict(lambda: defaultdict(int))
    play(tiles, computer, [0], trace=False)


code1()
code2()
