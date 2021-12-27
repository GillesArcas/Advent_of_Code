import re
import functools
import itertools
from collections import defaultdict


EXAMPLES1 = (
    ("""\
    Player 1 starting position: 4
    Player 2 starting position: 8""", 739785),
)

EXAMPLES2 = (
    ("""\
    Player 1 starting position: 4
    Player 2 starting position: 8""", 444356092776315),
)

INPUT = \
    """\
    Player 1 starting position: 9
    Player 2 starting position: 10"""


def read_data(s):
    line1, line2 = s.splitlines()
    match1 = re.match(r'\s*Player 1 starting position: (\d+)', line1)
    match2 = re.match(r'\s*Player 2 starting position: (\d+)', line2)
    return int(match1.group(1)), int(match2.group(1))


def detdie():
    n = 0
    while 1:
        yield n + 1
        n = (n + 1) % 100


def code1(data):
    player1, player2 = data
    score1, score2 = 0, 0
    die = detdie()

    for niter in range(1_000_000_000):
        ndie = next(die) + next(die) + next(die)
        player1 = (player1 - 1 + ndie) % 10 + 1
        score1 += player1
        # print(ndie, score1)
        if score1 >= 1000:
            rolls = (niter + 1) * 6 - 3
            return rolls * score2

        ndie = next(die) + next(die) + next(die)
        player2 = (player2 - 1 + ndie) % 10 + 1
        score2 += player2
        # print(ndie, score2)
        if score2 >= 1000:
            rolls = (niter + 1) * 6
            return rolls * score1
    return None


OCCSUM = {3:1, 4:3, 5:6, 6:7, 7:6, 8:3, 9:1}


@functools.lru_cache()
def play(player, player1, player2, score1, score2, die):
    # print(player, player1, player2, score1, score2, die)
    if player == 1:
        player1 = (player1 - 1 + die) % 10 + 1
        score1 += player1
        if score1 >= 21:
            return 1, 0
        else:
            win1, win2 = 0, 0
            for die, occurences in OCCSUM.items():
                w1, w2 = play(2, player1, player2, score1, score2, die)
                win1 += occurences * w1
                win2 += occurences * w2
            return win1, win2
    else:
        player2 = (player2 - 1 + die) % 10 + 1
        score2 += player2
        if score2 >= 21:
            return 0, 1
        else:
            win1, win2 = 0, 0
            for die, occurences in OCCSUM.items():
                w1, w2 = play(1, player1, player2, score1, score2, die)
                win1 += occurences * w1
                win2 += occurences * w2
            return win1, win2


def code2(data):
    # 11 minutes
    player1, player2 = data
    win1, win2 = 0, 0
    for die, occurences in OCCSUM.items():
        w1, w2 = play(1, player1, player2, 0, 0, die)
        win1 += occurences * w1
        win2 += occurences * w2
    return max(win1, win2)


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
