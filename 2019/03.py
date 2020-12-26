from collections import defaultdict


DATA = '03.txt'


def read_data(data):
    with open(data) as f:
        return [line.strip() for line in f.readlines()]


def draw_path(grid, s, label):
    i = j = distance = 0
    grid[(i, j)][label] = 0
    for step in s.split(','):
        direction = step[0]
        length = int(step[1:])
        delta_i = {'U': -1, 'D': 1, 'L': 0, 'R': 0}
        delta_j = {'U': 0, 'D': 0, 'L': -1, 'R': 1}
        for _ in range(1, length + 1):
            i, j, distance = i + delta_i[direction], j + delta_j[direction], distance + 1
            if label in grid[(i, j)]:
                grid[(i, j)][label] = min(grid[(i, j)][label], distance)
            else:
                grid[(i, j)][label] = distance


def crossing_distance(s1, s2):
    grid = defaultdict(dict)
    draw_path(grid, s1, 1)
    draw_path(grid, s2, 2)
    distmin = float('inf')
    for loc, labels in grid.items():
        if loc != (0, 0) and 1 in labels and 2 in labels:
            distmin = min(distmin, abs(loc[0]) + abs(loc[1]))
    return distmin


def shortest_distance(s1, s2):
    grid = defaultdict(dict)
    draw_path(grid, s1, 1)
    draw_path(grid, s2, 2)
    distmin = float('inf')
    for loc, labels in grid.items():
        if loc != (0, 0) and 1 in labels and 2 in labels:
            distmin = min(distmin, labels[1] + labels[2])
    return distmin


def code1():
    assert crossing_distance('R8,U5,L5,D3', 'U7,R6,D4,L4') == 6
    assert crossing_distance('R75,D30,R83,U83,L12,D49,R71,U7,L72', 'U62,R66,U55,R34,D71,R55,D58,R83') == 159
    assert crossing_distance('R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51', 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7') == 135
    print('>', crossing_distance(*read_data(DATA)))


def code2():
    assert shortest_distance('R8,U5,L5,D3', 'U7,R6,D4,L4') == 30
    assert shortest_distance('R75,D30,R83,U83,L12,D49,R71,U7,L72', 'U62,R66,U55,R34,D71,R55,D58,R83') == 610
    assert shortest_distance('R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51', 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7') == 410
    print('>', shortest_distance(*read_data(DATA)))


code1()
code2()
