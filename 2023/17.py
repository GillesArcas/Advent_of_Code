"""
--- Day 17: Clumsy Crucible ---
"""


import heapq
from collections import defaultdict


EXAMPLES1 = (
    ('17-exemple1.txt', 102),
)

EXAMPLES2 = (
    ('17-exemple1.txt', 94),
    ('17-exemple2.txt', 71),
)

INPUT = '17.txt'


def read_data(filename):
    with open(filename) as f:
        return [_.strip() for _ in f.readlines()]


def valid_coord(i, j, grid):
    return 0 <= i < len(grid) and 0 <= j < len(grid[0])


def neighbours(i, j, grid):
    neighs = []
    for i2, j2 in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
        if valid_coord(i2, j2, grid):
            neighs.append((i2, j2))
    return neighs


def grid_to_graph_1(grid):
    graph = defaultdict(dict)

    for i, line in enumerate(grid):
        for j, _ in enumerate(line):
            # down
            if i + 1 < len(grid):
                w = int(grid[i + 1][j])
                graph[i, j, 0, 0][i + 1, j, 1, 0] = w
                graph[i, j, 1, 0][i + 1, j, 2, 0] = w
                graph[i, j, 2, 0][i + 1, j, 3, 0] = w
                graph[i, j, 0, 1][i + 1, j, 1, 0] = w
                graph[i, j, 0, 2][i + 1, j, 1, 0] = w
                graph[i, j, 0, 3][i + 1, j, 1, 0] = w
                graph[i, j, 0,-1][i + 1, j, 1, 0] = w
                graph[i, j, 0,-2][i + 1, j, 1, 0] = w
                graph[i, j, 0,-3][i + 1, j, 1, 0] = w
            # up
            if i > 0:
                w = int(grid[i - 1][j])
                graph[i, j,-1, 0][i - 1, j,-2, 0] = w
                graph[i, j,-2, 0][i - 1, j,-3, 0] = w
                graph[i, j, 0, 1][i - 1, j,-1, 0] = w
                graph[i, j, 0, 2][i - 1, j,-1, 0] = w
                graph[i, j, 0, 3][i - 1, j,-1, 0] = w
                graph[i, j, 0,-1][i - 1, j,-1, 0] = w
                graph[i, j, 0,-2][i - 1, j,-1, 0] = w
                graph[i, j, 0,-3][i - 1, j,-1, 0] = w
            # right
            if j + 1 < len(line):
                w = int(grid[i][j + 1])
                graph[i, j, 0, 0][i, j + 1, 0, 1] = w
                graph[i, j, 1, 0][i, j + 1, 0, 1] = w
                graph[i, j, 2, 0][i, j + 1, 0, 1] = w
                graph[i, j, 3, 0][i, j + 1, 0, 1] = w
                graph[i, j,-1, 0][i, j + 1, 0, 1] = w
                graph[i, j,-2, 0][i, j + 1, 0, 1] = w
                graph[i, j,-3, 0][i, j + 1, 0, 1] = w
                graph[i, j, 0, 1][i, j + 1, 0, 2] = w
                graph[i, j, 0, 2][i, j + 1, 0, 3] = w
            # left
            if j > 0:
                w = int(grid[i][j - 1])
                graph[i, j, 1, 0][i, j - 1, 0,-1] = w
                graph[i, j, 2, 0][i, j - 1, 0,-1] = w
                graph[i, j, 3, 0][i, j - 1, 0,-1] = w
                graph[i, j,-1, 0][i, j - 1, 0,-1] = w
                graph[i, j,-2, 0][i, j - 1, 0,-1] = w
                graph[i, j,-3, 0][i, j - 1, 0,-1] = w
                graph[i, j, 0,-1][i, j - 1, 0,-2] = w
                graph[i, j, 0,-2][i, j - 1, 0,-3] = w
    return dict(graph)


def grid_to_graph_2(grid):
    graph = defaultdict(dict)

    for i, line in enumerate(grid):
        for j, _ in enumerate(line):
            # down
            if i + 1 < len(grid):
                w = int(grid[i + 1][j])
                for k in range(10):
                    graph[i, j, k, 0][i + 1, j, k + 1, 0] = w
                for k in range(4, 11):
                    graph[i, j, 0, k][i + 1, j, 1, 0] = w
                    graph[i, j, 0,-k][i + 1, j, 1, 0] = w
            # up
            if i > 0:
                w = int(grid[i - 1][j])
                for k in range(10):
                    graph[i, j, -k, 0][i - 1, j, -k - 1, 0] = w
                for k in range(4, 11):
                    graph[i, j, 0, k][i - 1, j, -1, 0] = w
                    graph[i, j, 0,-k][i - 1, j, -1, 0] = w
            # right
            if j + 1 < len(line):
                w = int(grid[i][j + 1])
                for k in range(10):
                    graph[i, j, 0, k][i, j + 1, 0, k + 1] = w
                for k in range(4, 11):
                    graph[i, j, k, 0][i, j + 1, 0, 1] = w
                    graph[i, j,-k, 0][i, j + 1, 0, 1] = w
            # left
            if j > 0:
                w = int(grid[i][j - 1])
                for k in range(10):
                    graph[i, j, 0, -k][i, j - 1, 0, -k - 1] = w
                for k in range(4, 11):
                    graph[i, j, k, 0][i, j - 1, 0, -1] = w
                    graph[i, j,-k, 0][i, j - 1, 0, -1] = w
    return dict(graph)


def dijkstra(graph, start, is_end):
    routes = []
    heapq.heappush(routes, (0, start))
    came_from = {}
    came_from[start] = None
    cost_so_far = {}
    cost_so_far[start] = 0

    while routes:
        dist, node = heapq.heappop(routes)

        if is_end(node):
            return dist, node, came_from

        if node not in graph:
            continue
        for node2 in graph[node]:
            newdist = cost_so_far[node] + graph[node][node2]
            if node2 not in cost_so_far or newdist < cost_so_far[node2]:
                cost_so_far[node2] = newdist
                came_from[node2] = node
                heapq.heappush(routes, (newdist, node2))

    return float('inf'), None, None


def print_grid_and_path(grid, came_from, end):
    grid = [list(line) for line in grid]
    node = end
    while tuple(node[:2]) != (0, 0):
        grid[node[0]][node[1]] = '#'
        node = came_from[node]

    for line in grid:
        print(''.join(line))


def code1(grid):
    graph = grid_to_graph_1(grid)
    start = (0, 0, 0, 0)
    end = (len(grid) - 1, len(grid[0]) - 1)

    def is_end(node):
        return tuple(node[:2]) == end

    dist, end, came_from = dijkstra(graph, start, is_end)
    if 0:
        print_grid_and_path(grid, came_from, end)
    return dist


def code2(grid):
    graph = grid_to_graph_2(grid)
    start = (0, 0, 0, 0)
    end = (len(grid) - 1, len(grid[0]) - 1)

    def is_end(node):
        return tuple(node[:2]) == end and (node[2] >= 4 or node[3] >= 4)

    dist, end, came_from = dijkstra(graph, start, is_end)
    if 0:
        print_grid_and_path(grid, came_from, end)
    return dist


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
