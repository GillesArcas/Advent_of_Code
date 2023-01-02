"""
--- 2016 --- Day 13: A Maze of Twisty Little Cubicles ---

Keywords: dijkstra
"""


import heapq


EXAMPLES1 = (
    ('13-exemple1.txt', 11),
)

EXAMPLES2 = (
)

INPUT = '13.txt'


def read_data(filename):
    with open(filename) as f:
        numbers = [int(_) for _ in f.read().split(',')]
    return numbers


def make_grid(favorite, xtarget, ytarget, margin):
    grid = [['.' for _ in range(xtarget + margin)] for _ in range(ytarget + margin)]
    for x in range(xtarget + margin):
        for y in range(ytarget + margin):
            b = bin(x*x + 3*x + 2*x*y + y + y*y + favorite)[2:]
            if sum(_ == '1' for _ in b) % 2:
                grid[y][x] = '#'
    return grid


def print_grid(grid):
    for line in grid:
        print(''.join(line))
    print()


def make_graph(grid, xtarget, ytarget, margin):
    graph = {}
    for x in range(xtarget + margin):
        for y in range(ytarget + margin):
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
    favorite, xtarget, ytarget = data
    margin = 3 if favorite == 10 else 10
    grid = make_grid(favorite, xtarget, ytarget, margin)
    print_grid(grid)
    graph = make_graph(grid, xtarget, ytarget, margin)
    start = (1, 1)
    end = xtarget, ytarget
    dist, _ = dijkstra(graph, start, end)
    return dist


def code2(data):
    favorite, xtarget, ytarget = data
    margin = 3 if favorite == 10 else 10
    grid = make_grid(favorite, xtarget, ytarget, margin)
    graph = make_graph(grid, xtarget, ytarget, margin)
    start = (1, 1)
    count = 1  # count starting point
    for x in range(xtarget + margin):
        for y in range(ytarget + margin):
            if grid[y][x] == '.':
                end = x, y
                dist, _ = dijkstra(graph, start, end)
                if dist <= 50:
                    count += 1
    return count


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
