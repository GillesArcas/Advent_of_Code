"""
--- 2022 --- Day 24: Blizzard Basin ---

Keywords: dijkstra
"""


import heapq
from collections import defaultdict


EXAMPLES1 = (
    ('24-exemple1.txt', 18),
)

EXAMPLES2 = (
    ('24-exemple1.txt', 54),
)

INPUT = '24.txt'


def read_data(filename):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines()]

    grid = [['.' for elem in line[1:-1]] for line in lines[1:-1]]
    for i, line in enumerate(lines[1:-1]):
        for j, char in enumerate(line[1:-1]):
            if char != '.':
                grid[i][j] = char

    return grid


def next_grid(grid):
    imax = len(grid) - 1
    jmax = len(grid[0]) - 1
    newgrid = [['.' for elem in line] for line in grid]

    for i, line in enumerate(grid):
        for j, elem in enumerate(line):
            if elem != '.':
                for bliz in elem:
                    if bliz == '^':
                        i2, j2 = imax if i == 0 else i - 1, j
                    elif bliz == 'v':
                        i2, j2 = 0 if i == imax else i + 1, j
                    elif bliz == '<':
                        i2, j2 = i, jmax if j == 0 else j - 1
                    elif bliz == '>':
                        i2, j2 = i, 0 if j == jmax else j + 1
                    else:
                        assert 0
                    if newgrid[i2][j2] == '.':
                        newgrid[i2][j2] = []
                    newgrid[i2][j2].append(bliz)

    return newgrid


def print_grid(grid):
    for line in grid:
        textline = []
        for elem in line:
            if elem == '.':
                textline.append(elem)
            elif len(elem) == 1:
                textline.append(elem[0])
            else:
                textline.append(str(len(elem)))
        print(''.join(textline))
    print()


def dijkstra(graph, start, end):
    routes = []
    heapq.heappush(routes, (0, start))
    came_from = dict()
    came_from[start] = None
    cost_so_far = dict()
    cost_so_far[start] = 0

    while routes:
        dist, node = heapq.heappop(routes)

        if node == end:
            return dist, node

        for node2 in graph[node]:
            newdist = cost_so_far[node] + graph[node][node2]
            if node2 not in cost_so_far or newdist < cost_so_far[node2]:
                cost_so_far[node2] = newdist
                came_from[node2] = node
                heapq.heappush(routes, (newdist, node2))

    return float('inf'), None


def neighbours(i, j, grid):
    neighs = []
    for i2, j2 in ((i, j), (i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
        if 0 <= i2 < len(grid) and 0 <= j2 < len(grid[0]) and grid[i2][j2] == '.':
            neighs.append((i2, j2))
    return neighs


def travel(grid):
    graph = defaultdict(lambda: dict())
    time = 0
    start = (0, -1, 0)
    while True:
        nextgrid = next_grid(grid)
        time += 1
        # print(time)
        if nextgrid[0][0] == '.':
            graph[start][(time, 0, 0)] = 1

        for i, line in enumerate(grid):
            for j, elem in enumerate(line):
                if elem == '.':
                    for i2, j2 in neighbours(i, j, nextgrid):
                        graph[(time - 1, i, j)][(time, i2, j2)] = 1

        end = (time, len(grid), len(grid[0]) - 1)

        if grid[len(grid) - 1][len(grid[0]) - 1] == '.':
            graph[(time - 1, len(grid) - 1, len(grid[0]) - 1)][end] = 1

        dist, _ = dijkstra(graph, start, end)
        if dist < float('inf'):
            return time, nextgrid

        grid = nextgrid

    return None, None


def travel_back(grid):
    graph = defaultdict(lambda: dict())
    time = 0
    start = (0, len(grid), len(grid[0]) - 1)
    while True:
        nextgrid = next_grid(grid)
        time += 1
        # print(time)
        if nextgrid[len(grid) - 1][len(grid[0]) - 1] == '.':
            graph[start][(time, len(grid) - 1, len(grid[0]) - 1)] = 1

        for i, line in enumerate(grid):
            for j, elem in enumerate(line):
                if elem == '.':
                    for i2, j2 in neighbours(i, j, nextgrid):
                        graph[(time - 1, i, j)][(time, i2, j2)] = 1

        end = (time, -1, 0)

        if grid[0][0] == '.':
            graph[(time - 1, 0, 0)][end] = 1

        dist, _ = dijkstra(graph, start, end)
        if dist < float('inf'):
            return time, nextgrid

        grid = nextgrid

    return None, None


def code1(grid):
    time, _ = travel(grid)
    return time


def code2(grid):
    time1, grid = travel(grid)
    time2, grid = travel_back(grid)
    time3, grid = travel(grid)
    return time1 + time2 + time3


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
