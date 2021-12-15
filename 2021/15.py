import sortedcontainers
from collections import Counter, defaultdict


EXAMPLES1 = (
    ('15-exemple1.txt', 40),
)

EXAMPLES2 = (
    ('15-exemple1.txt', 315),
)

INPUT =  '15.txt'


def neighbours(cost, i, j):
    neigh = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
    neigh = [(i, j) for i, j in neigh if 0 <= i< len(cost) and 0 <= j< len(cost[0])]
    return neigh


def graph(cost):
    edges = defaultdict(lambda: defaultdict(int))
    for i in range(len(cost)):
        for j in range(len(cost[0])):
            for i2, j2 in neighbours(cost, i, j):
                edges[(i, j)][(i2, j2)] = cost[i2][j2]
    return edges


def read_data(fn):
    cost = list()
    with open(fn) as f:
        for line in f:
            line = line.strip()
            cost.append([int(_) for _ in list(line)])
    return graph(cost), cost


def code1(data):
    edges, cost = data
    return dijkstra(edges, (0, 0), (len(cost) - 1, len(cost[0]) - 1))


def dijkstra(edges, start, end):
    dist = dict()
    for node in edges:
        dist[node] = float('inf')
    dist[start] = 0

    nodes = set(edges)
    while nodes:
        node = min(nodes, key=lambda x:dist[x])
        if node is None:
            nodes.clear()
        else:
            nodes.remove(node)
            for node2 in edges[node]:
                newdist = dist[node] + edges[node][node2]
                if newdist < dist[node2]:
                    dist[node2] = newdist

    return dist[end]


def dijkstra(edges, start, end):
    dist = dict()
    for node in edges:
        dist[node] = float('inf')
    dist[start] = 0

    nodes = sortedcontainers.SortedList(edges, lambda x:dist[x])
    while nodes:
        node = nodes.pop(0)
        if node is None:
            nodes.clear()
        else:
            for node2 in edges[node]:
                newdist = dist[node] + edges[node][node2]
                if newdist < dist[node2]:
                    nodes.remove(node2)
                    dist[node2] = newdist
                    nodes.add(node2)

    return dist[end]


def incrcost(cost):
    new = [line[:] for line in cost]

    for i in range(len(cost)):
        for j in range(len(cost[0])):
            new[i][j] = new[i][j] + 1
            if new[i][j] == 10:
                new[i][j] = 1
    return new


def code2(data):
    edges, cost = data

    costs = [[None for x in range(5)] for y in range(5)]
    for i in range(5):
        for j in range(5):
            if i == j == 0:
                costs[i][j] = cost
            elif j == 0:
                costs[i][j] = incrcost(costs[i - 1][j])
            else:
                costs[i][j] = incrcost(costs[i][j - 1])

    dimx = len(cost[0])
    dimy = len(cost)
    fullcost = [[None for x in range(5 * dimx)] for y in range(5 * dimy)]
    for y in range(len(fullcost)):
        for x in range(len(fullcost[0])):
            fullcost[y][x] = costs[y // dimy][x // dimx][y % dimy][x % dimx]

    edges = graph(fullcost)
    return dijkstra(edges, (0, 0), (len(fullcost) - 1, len(fullcost[0]) - 1))


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
