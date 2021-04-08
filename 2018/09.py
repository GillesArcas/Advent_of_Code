import re


DATA = """\
     9 players; last marble is worth    25 points: high score is 32
    10 players; last marble is worth  1618 points: high score is 8317
    13 players; last marble is worth  7999 points: high score is 146373
    17 players; last marble is worth  1104 points: high score is 2764
    21 players; last marble is worth  6111 points: high score is 54718
    30 players; last marble is worth  5807 points: high score is 37305
   479 players; last marble is worth 71035 points: high score is 0
""".splitlines()


def read_data(n):
    line = DATA[n]
    match = re.search(r'(\d+) players; last marble is worth\s*(\d+) points: high score is (\d+)', line)
    players, last_marble, score = match.group(1, 2, 3)
    return int(players), int(last_marble), int(score)


def insert_next(circle, current, marble):
    #print('>', len(circle), current, marble)
    if current + 2 == len(circle):
        circle.append(marble)
        current = len(circle) - 1
    else:
        current = (current + 2) % len(circle)
        circle.insert(current, marble)
    #print('<', len(circle), current, marble)
    return current


def play(players, last_marble):
    scores = [0] * players
    player = 0
    circle = [0, 1]
    current = 1
    for marble in range(2, last_marble + 1):
        if marble % 1000 == 0:
            print(marble, last_marble)
        player = (player + 1) % players
        if marble % 23 == 0:
            scores[player] += marble
            current = (current - 7) % len(circle)
            scores[player] += circle.pop(current)
        else:
            current = insert_next(circle, current, marble)

        # print('[%d]' % (player + 1,) , ' '.join('%2d' % _ for _ in circle), '-', scores[player])

    return max(scores)


def code1():
    for _ in range(len(DATA)):
        players, last_marble, expected_score = read_data(_)
        score = play(players, last_marble)
        if expected_score:
            assert score == expected_score
        else:
            print('1>', score)


def code2():
    players, last_marble, expected_score = read_data(len(DATA) - 1)
    score = play(players, last_marble * 100)
    print('2>', score)


code1()
code2()
