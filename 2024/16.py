"""
--- Day 16: Reindeer Maze ---
"""


import heapq


EXAMPLES1 = (
    ('16-exemple1.txt', 7036),
    ('16-exemple2.txt', 11048),
)

EXAMPLES2 = (
    ('16-exemple1.txt', 45),
    ('16-exemple2.txt', 64),
)

INPUT = '16.txt'


TURNL = {'<': 'v', '>': '^', '^': '<', 'v': '>'}
TURNR = {'<': '^', '>': 'v', '^': '>', 'v': '<'}
IDELTA = {'<': 0, '>': 0, '^': -1, 'v': 1}
JDELTA = {'<': -1, '>': 1, '^': 0, 'v': 0}


def read_data(filename):
    with open(filename) as f:
        maze = [_.strip() for _ in f.readlines()]

    nodes = {}
    for i, line in enumerate(maze):
        for j, char in enumerate(line):
            if char == 'S':
                start = (i, j, '>')
            if char == 'E':
                end = ((i, j, '>'), (i, j, '<'), (i, j, '^'), (i, j, 'v'))
            if char != '#':
                for d in '^v<>':
                    nodes[i, j, d] = {(i, j, TURNL[d]): 1000, (i, j, TURNR[d]): 1000}
                    if maze[i + IDELTA[d]][j + JDELTA[d]] != '#':
                        nodes[i, j, d][i + IDELTA[d], j + JDELTA[d], d] = 1
            if char == 'S':
                start = (i, j, '>')
            if char == 'E':
                for node in ((i, j, '>'), (i, j, '<'), (i, j, '^'), (i, j, 'v')):
                    nodes[node][i, j] = 0
                end = (i, j)
                nodes[end] = {}

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
            return dist, node, came_from

        for node2 in graph[node]:
            newdist = cost_so_far[node] + graph[node][node2]
            if node2 not in cost_so_far or newdist < cost_so_far[node2]:
                cost_so_far[node2] = newdist
                came_from[node2] = {node}
                heapq.heappush(routes, (newdist, node2))
            if newdist == cost_so_far[node2]:
                came_from[node2].add(node)

    return float('inf'), None, came_from


def code1(data):
    nodes, start, end = data
    dist, _, _ = dijkstra(nodes, start, end)
    return dist


def scan_came_from(came_from, node, bestnodes):
    bestnodes.add(node[:2])
    if came_from[node]:
        for x in came_from[node]:
            scan_came_from(came_from, x, bestnodes)


def code2(data):
    nodes, start, end = data
    _, _, came_from = dijkstra(nodes, start, end)
    bestnodes = set()
    scan_came_from(came_from, end, bestnodes)
    return len(bestnodes)


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
