"""
--- 2016 --- Day 24: Air Duct Spelunking ---

Keywords: dijkstra
"""


import heapq
import itertools


EXAMPLES1 = (
    ('24-exemple1.txt', 14),
)

EXAMPLES2 = (
)

INPUT = '24.txt'


def read_data(filename):
    grid = []
    with open(filename) as f:
        for line in [_.strip() for _ in f]:
            grid.append(list(line))
    locations = {}
    for y, line in enumerate(grid):
        for x, char in enumerate(line):
            if char.isdigit():
                grid[y][x] = '.'
                locations[int(char)] = (x, y)
    return grid, locations


def print_grid(grid):
    for line in grid:
        print(''.join(line))
    print()


def make_graph(grid):
    graph = {}
    for x in range(len(grid[0])):
        for y in range(len(grid)):
            if grid[y][x] == '.':
                graph[(x, y)] = {}
                for xx, yy in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                    if 0 <= xx < len(grid[0]) and 0 <= yy < len(grid):
                        if grid[yy][xx] == '.':
                            graph[(x, y)][(xx, yy)] = 1
    return graph


def dijkstra(graph, start, end):
    """
    graph is a dict of dict: graph[node1][node2] = distance(node1, node2)
    start and end must be different
    """
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

    return float('inf'), []


def code1(data):
    grid, locations = data
    graph = make_graph(grid)
    locmax = max(locations)
    dist = [[0 for _ in range(locmax + 1)] for _ in range(locmax + 1)]
    for loc in range(locmax + 1):
        for loc2 in range(locmax + 1):
            d, _ = dijkstra(graph, locations[loc], locations[loc2])
            dist[loc][loc2] = d

    dmin = float('inf')
    for path in itertools.permutations(list(range(1, locmax + 1)), locmax):
        d = dist[0][path[0]]
        for x, y in zip(path, path[1:]):
            d += dist[x][y]
        if d < dmin:
            dmin = d

    return dmin


def code2(data):
    grid, locations = data
    graph = make_graph(grid)
    locmax = max(locations)
    dist = [[0 for _ in range(locmax + 1)] for _ in range(locmax + 1)]
    for loc in range(locmax + 1):
        for loc2 in range(locmax + 1):
            d, _ = dijkstra(graph, locations[loc], locations[loc2])
            dist[loc][loc2] = d

    dmin = float('inf')
    for path in itertools.permutations(list(range(1, locmax + 1)), locmax):
        path2 = path + (0,)
        d = dist[0][path2[0]]
        for x, y in zip(path2, path2[1:]):
            d += dist[x][y]
        if d < dmin:
            dmin = d

    return dmin


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
