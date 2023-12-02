"""
--- Day 2: Cube Conundrum ---
"""


import re
import math


EXAMPLES1 = (
    ('02-exemple1.txt', 8),
)

EXAMPLES2 = (
    ('02-exemple1.txt', 2286),
)

INPUT = '02ord.txt'


def read_data(filename):
    with open(filename) as f:
        lines = f.readlines()

    games = []
    for index, line in enumerate(lines):
        match = re.match(r'Game (\d+): (.*)', line)
        game_id = int(match.group(1))
        assert game_id == index + 1
        subsets = match.group(2).split(';')
        game_subsets = []
        for subset in subsets:
            match_red = re.search(r'(\d+) red', subset)
            match_green = re.search(r'(\d+) green', subset)
            match_blue = re.search(r'(\d+) blue', subset)
            outcome = (
                (0 if not match_red else int(match_red.group(1))),
                (0 if not match_green else int(match_green.group(1))),
                (0 if not match_blue else int(match_blue.group(1))))
            game_subsets.append(outcome)
        games.append(game_subsets)
    return games


def code1(games):
    total_ids = 0
    for gameid, game_subsets in enumerate(games, 1):
        if all(r <= 12 and g <= 13 and b <= 14 for r, g, b in game_subsets):
            total_ids += gameid
    return total_ids


def code2(games):
    powersum = 0
    for game_subsets in games:
        gamepower = math.prod([max(values) for values in zip(*game_subsets)])
        powersum += gamepower
    return powersum


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
