"""
--- 2022 --- Day 2: Rock Paper Scissors ---
"""


EXAMPLES1 = (
    ('02-exemple1.txt', 15),
)

EXAMPLES2 = (
    ('02-exemple1.txt', 12),
)

INPUT = '02.txt'


def read_data(filename):
    with open(filename) as f:
        lines = f.readlines()
    return [_.strip().split() for _ in lines]


WINNER = {'AX':'0', 'AY':'Y', 'AZ':'A',
          'BX':'B', 'BY':'0', 'BZ':'Z',
          'CX':'X', 'CY':'C', 'CZ':'0'}

MOVE_SCORE = {'X':1, 'Y':2, 'Z':3}


def my_score1(round):
    winner = WINNER[round[0] + round[1]]
    round_score = 3 if winner == '0' else 0 if winner in 'ABC' else 6
    return MOVE_SCORE[round[1]] + round_score


def my_score2(round):
    winners = {'X':'ABC', 'Y':'0', 'Z':'XYZ'}[round[1]]
    my_move = [_ for _ in 'XYZ' if WINNER[round[0] + _] in winners][0]
    return my_score1((round[0], my_move))


def code1(rounds):
    return sum(my_score1(_) for _ in rounds)


def code2(rounds):
    return sum(my_score2(_) for _ in rounds)


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
