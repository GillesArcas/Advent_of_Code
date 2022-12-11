"""
--- 2018 --- Day 22: Mode Maze ---

Keywords: dijkstra
"""


import re
import heapq


EXAMPLES1 = (
    ('depth: 510\ntarget: 10,10', 114),
)

EXAMPLES2 = (
    ('depth: 510\ntarget: 10,10', 45),
)

INPUT = 'depth: 5616\ntarget: 10,785'


def read_data(string):
    match = re.match(r'depth: (\d+)\ntarget: (\d+),(\d+)', string)
    depth, xtarget, ytarget = [int(_) for _ in (match.group(1), match.group(2), match.group(3))]

    # magic value
    margin = 40

    # geol_grid[y][x] = geologic_index(x, y)
    # eros_grid[y][x] = erosion_level(x, y)
    # risk_grid[y][x] = risk_level(x, y)
    geol_grid = [[None for _ in range(xtarget + 1 + margin)] for _ in range(ytarget + 1 + margin)]
    eros_grid = [[None for _ in range(xtarget + 1 + margin)] for _ in range(ytarget + 1 + margin)]
    risk_grid = [[None for _ in range(xtarget + 1 + margin)] for _ in range(ytarget + 1 + margin)]

    geol_grid[0][0] = 0
    eros_grid[0][0] = (geol_grid[0][0] + depth) % 20183
    for x in range(xtarget + 1 + margin):
        geol_grid[0][x] = x * 16807
        eros_grid[0][x] = (geol_grid[0][x] + depth) % 20183
    for y in range(ytarget + 1 + margin):
        geol_grid[y][0] = y * 48271
        eros_grid[y][0] = (geol_grid[y][0] + depth) % 20183
    for y in range(1, ytarget + 1 + margin):
        for x in range(1, xtarget + 1 + margin):
            geol_grid[y][x] = eros_grid[y - 1][x] * eros_grid[y][x - 1]
            eros_grid[y][x] = (geol_grid[y][x] + depth) % 20183
    geol_grid[ytarget][xtarget] = 0
    eros_grid[ytarget][xtarget] = (geol_grid[ytarget][xtarget] + depth) % 20183

    # set grids again with geologic index 0 at target
    for y in range(ytarget, ytarget + 1 + margin):
        for x in range(xtarget, xtarget + 1 + margin):
            if (x, y) != (xtarget, ytarget):
                geol_grid[y][x] = eros_grid[y - 1][x] * eros_grid[y][x - 1]
                eros_grid[y][x] = (geol_grid[y][x] + depth) % 20183

    for y in range(0, ytarget + 1 + margin):
        for x in range(0, xtarget + 1 + margin):
            risk_grid[y][x] = eros_grid[y][x] % 3

    # print_risk(xtarget, ytarget, risk_grid, margin)
    # print()

    return xtarget, ytarget, risk_grid, margin


def print_risk(xtarget, ytarget, risk_grid):
    for y, line in enumerate(risk_grid):
        if y == 0:
            line = line.copy()
            line = ['.=|'[_] for _ in line]
            line[0] = 'M'
        elif y == ytarget:
            line = line.copy()
            line = ['.=|'[_] for _ in line]
            line[xtarget] = 'T'
        else:
            line = ['.=|'[_] for _ in line]
        print(''.join(line))


def risk_index(xtarget, ytarget, risk_grid):
    risk = 0
    for y in range(0, ytarget + 1):
        for x in range(0, xtarget + 1):
            risk += risk_grid[y][x]
    return risk


TOOLS = {0: {'G', 'T'}, 1: {'G', '0'}, 2: {'T', '0'}}
INF = float('inf')


def neighbours(x, y, xtarget, ytarget, margin):
    neigh = []
    for xx, yy in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
        if 0 <= xx <= xtarget + margin and 0 <= yy <= ytarget + margin:
            neigh.append((xx, yy))
    return neigh


def grid_to_graph(xtarget, ytarget, risk_grid, margin):
    graph = {}
    for y in range(0, ytarget + 1 + margin):
        for x in range(0, xtarget + 1 + margin):
            geol1 = risk_grid[y][x]
            for tool1 in TOOLS[geol1]:
                graph[(x, y, tool1)] = {}
                for tool2 in TOOLS[geol1]:
                    if tool2 != tool1:
                        graph[(x, y, tool1)][(x, y, tool2)] = 7
                for xx, yy in neighbours(x, y, xtarget, ytarget, margin):
                    geol2 = risk_grid[yy][xx]
                    if tool1 in TOOLS[geol2]:
                        graph[(x, y, tool1)][(xx, yy, tool1)] = 1
    return graph


def dijkstra(graph, start, end=None):
    # https://github.com/vterron/dijkstra/blob/master/dijkstra.py

    routes = []
    for node in graph[start]:
        heapq.heappush(routes, (graph[start][node], node))

    visited = set()
    visited.add(start)

    while routes:
        dist, node = heapq.heappop(routes)
        if node in visited:
            continue

        if node == end:
            return dist

        for node2 in graph[node]:
            if node2 not in visited:
                newdist = dist + graph[node][node2]
                heapq.heappush(routes, (newdist, node2))

        visited.add(node)


def dijkstra(graph, start, end=None):
    # https://github.com/vterron/dijkstra/blob/master/dijkstra.py

    routes = []
    for node in graph[start]:
        heapq.heappush(routes, (graph[start][node], [start, node]))

    visited = set()
    visited.add(start)

    while routes:
        dist, path = heapq.heappop(routes)
        node = path[-1]
        if node in visited:
            continue

        if node == end:
            return dist, path

        for node2 in graph[node]:
            if node2 not in visited:
                newdist = dist + graph[node][node2]
                newpath = path + [node2]
                heapq.heappush(routes, (newdist, newpath))

        visited.add(node)


def code1(data):
    xtarget, ytarget, risk_grid, _ = data
    return risk_index(xtarget, ytarget, risk_grid)


def code2(data):
    xtarget, ytarget, risk_grid, margin = data
    graph = grid_to_graph(xtarget, ytarget, risk_grid, margin)
    dist, _ = dijkstra(graph, (0, 0, 'T'), (xtarget, ytarget, 'T'))
    return dist


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
