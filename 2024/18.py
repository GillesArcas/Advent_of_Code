"""
--- Day 18: RAM Run ---
"""


import heapq


EXAMPLES1 = (
    ('18-exemple1.txt', 22),
)

EXAMPLES2 = (
    ('18-exemple1.txt', (6,1)),
)

INPUT = '18.txt'


def read_data(filename):
    with open(filename) as f:
        content = f.readlines()
    coords = []
    xmax = 0
    ymax = 0
    for line in content:
        coord = [int(_) for _ in line.strip().split(',')]
        coords.append(coord)
        xmax = max(xmax, coord[0])
        ymax = max(ymax, coord[1])
    mymap = [['.' for _ in range(xmax + 1)] for _ in range(ymax + 1)]
    return mymap, coords


def dijkstra(graph, start, end):
    routes = []
    heapq.heappush(routes, (0, start))
    came_from = {}
    came_from[start] = None
    cost_so_far = {}
    cost_so_far[start] = 0

    while routes:
        dist, node = heapq.heappop(routes)

        if node == end:
            return dist, node, came_from

        for node2 in graph[node]:
            newdist = cost_so_far[node] + graph[node][node2]
            if node2 not in cost_so_far or newdist < cost_so_far[node2]:
                cost_so_far[node2] = newdist
                came_from[node2] = node
                heapq.heappush(routes, (newdist, node2))

    return float('inf'), None, came_from


def code1(data):
    mymap, coords = data
    if len(mymap) == 7:
        n = 12
    else:
        n = 1024
    for x, y in coords[:n]:
        mymap[y][x] = '#'
    nodes = {}
    for i, line in enumerate(mymap):
        for j, char in enumerate(line):
            if char == '.':
                nodes[i, j] = {}
                for i2, j2 in ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)):
                    if 0 <= i2 < len(mymap) and 0 <= j2 < len(mymap[0]) and mymap[i2][j2] == '.':
                        nodes[i, j][i2, j2] = 1
    start = (0, 0)
    end = (len(mymap) - 1, len(mymap[0]) - 1)
    dist, _, _ = dijkstra(nodes, start, end)
    return dist


def code2(data):
    mymap, coords = data
    if len(mymap) == 7:
        n = 12
    else:
        n = 1024
    for x, y in coords[:n]:
        mymap[y][x] = '#'
    nodes = {}
    for i, line in enumerate(mymap):
        for j, char in enumerate(line):
            if char == '.':
                nodes[i, j] = {}
                for i2, j2 in ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)):
                    if 0 <= i2 < len(mymap) and 0 <= j2 < len(mymap[0]) and mymap[i2][j2] == '.':
                        nodes[i, j][i2, j2] = 1
    start = (0, 0)
    end = (len(mymap) - 1, len(mymap[0]) - 1)

    for j, i in coords[n:]:
        for i2, j2 in ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)):
            if (i2, j2) in nodes:
                del nodes[i2, j2][i, j]

        dist, _, _ = dijkstra(nodes, start, end)
        if dist == float('inf'):
            return j, i


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
