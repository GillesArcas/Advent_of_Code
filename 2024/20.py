"""
--- Day 20: Race Condition ---
"""


import heapq


EXAMPLES1 = (
    ('20-exemple1.txt', 10),
)

EXAMPLES2 = (
    ('20-exemple1.txt', 41),
)

INPUT = '20.txt'


def read_data(filename):
    with open(filename) as f:
        mymap = [line.strip() for line in f.readlines()]
    for i, line in enumerate(mymap):
        for j, char in enumerate(line):
            if char == 'S':
                start = i, j
            elif char == 'E':
                end = i, j

    nodes = {}
    for i, line in enumerate(mymap):
        for j, char in enumerate(line):
            if char != '#':
                nodes[i, j] = {}
                for ii, jj in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
                    if 0 <= ii < len(mymap) and 0 <= jj < len(mymap[0]) and mymap[ii][jj] != '#':
                        nodes[i, j][ii, jj] = 1

    return nodes, start, end


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
            return dist, came_from

        for node2 in graph[node]:
            newdist = cost_so_far[node] + graph[node][node2]
            if node2 not in cost_so_far or newdist < cost_so_far[node2]:
                cost_so_far[node2] = newdist
                came_from[node2] = node
                heapq.heappush(routes, (newdist, node2))

    return float('inf'), None


def proceed(data, cheat, target):
    nodes, start, end = data

    dist0, came_from = dijkstra(nodes, start, end)
    path = [end]
    node = end
    while node != start:
        node = came_from[node]
        path.insert(0, node)

    count = 0
    for i1, node1 in enumerate(path):
        for i2, node2 in enumerate(path):
            if i2 > i1:
                dist = abs(node1[0] - node2[0]) + abs(node1[1] - node2[1])
                if dist <= cheat:
                    if i2 - i1 - dist >= target:
                        count += 1

    return count


def code1(data):
    _, start, _ = data
    if start == (3, 1):
        target = 10
    else:
        target = 100
    return proceed(data, 2, target)


def code2(data):
    _, start, _ = data
    if start == (3, 1):
        target = 70
    else:
        target = 100
    return proceed(data, 20, target)


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
