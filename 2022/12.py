"""
--- 2022 --- Day 12: Hill Climbing Algorithm ---

Keywords: dijkstra
"""


import heapq


EXAMPLES1 = (
    ('12-exemple1.txt', 31),
)

EXAMPLES2 = (
    ('12-exemple1.txt', 29),
)

INPUT = '12.txt'


def neighbours(i, j, grid):
    neigh = ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1))
    return ((i, j) for i, j in neigh if 0 <= i < len(grid) and 0 <= j < len(grid[0]))


def find_char(grid, target):
    for i, line in enumerate(grid):
        for j, char in enumerate(line):
            if char == target:
                return (i, j)


def replace_char(grid, i, j, rep):
    line = list(grid[i])
    line[j] = rep
    grid[i] = ''.join(line)


def read_data(filename):
    with open(filename) as f:
        grid = [_.strip() for _ in f.readlines()]

    start = find_char(grid, 'S')
    end = find_char(grid, 'E')
    replace_char(grid, *start, 'a')
    replace_char(grid, *end, 'z')

    graph = {}
    for i, line in enumerate(grid):
        for j, char in enumerate(line):
            graph[(i, j)] = {}
            succ = chr(ord(char) + 1)
            for ii, jj in neighbours(i, j, grid):
                if grid[ii][jj] <= succ:
                    graph[(i, j)][(ii, jj)] = 1

    return start, end, graph, grid


def dijkstra(graph, start, end):
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


def dijkstra_(graph, start, end=None):
    # return paths, not used, should update neighbours to <= rather than >=
    routes = []
    for node in graph[start]:
        heapq.heappush(routes, (graph[start][node], [start, node]))

    visited = {}
    visited[start] = (0, [])

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

        visited[node] = (dist, path)

    return visited, []


def code1(data):
    start, end, graph, _ = data
    dist, _ = dijkstra(graph, start, end)
    return dist


def code2(data):
    _, end, graph, grid = data

    mini = float('inf')
    for i, line in enumerate(grid):
        for j, char in enumerate(line):
            if char == 'a':
                dist, _ = dijkstra(graph, (i, j), end)
                if dist < mini:
                    mini = dist

    return mini


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
