import copy
from collections import defaultdict


def getdata(n):
    if n == 0:
        filename = '20.txt'
        result = None
    elif n == 1:
        filename = '20-exemple1.txt'
        result = 23
    elif n == 2:
        filename = '20-exemple2.txt'
        result = 58
    elif n == 3:
        filename = '20-exemple1.txt'
        result = 26
    elif n == 4:
        filename = '20-exemple3.txt'
        result = 396
    else:
        assert 0

    with open(filename) as f:
        maze = [list(line.strip('\n')) for line in f.readlines()]

    return maze, result


DELTA_I = (0, -1, 0, 1)
DELTA_J = (1, 0, -1, 0)


def neighbours(maze, i, j):
    neigh = (i, j + 1), (i - 1, j), (i, j - 1), (i + 1, j)
    return [(p, q) for (p, q) in neigh if 0 <= p < len(maze) and 0 <= q < len(maze[0])]


def makemaze(n):
    maze, expected = getdata(n)
    maze2 = [line[:] for line in maze]

    # a pair of letters is transformed into a single letter
    # keys makes the conversion pair --> single letter
    # portals gives coordinates coordinates --> single letter
    # A and z are reserved for entry and exit of maze
    labels = list('BCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxy')
    portals = dict()
    keys = dict()

    for i, line in enumerate(maze):
        for j, x in enumerate(maze[0]):
            if maze[i][j] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                free = [(p, q) for (p, q) in neighbours(maze, i, j) if maze[p][q] == '.']
                if free:
                    free = free[0]
                    second = [(p, q) for (p, q) in neighbours(maze, i, j) if maze[p][q] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'][0]
                    key = makekey(maze, i, j, second[0], second[1])

                    if key == 'AA':
                        label = 'A'
                        keys['AA'] = 'A'
                    elif key == 'ZZ':
                        label = 'z'
                        keys['ZZ'] = 'z'
                    elif key in keys:
                        label = keys[key]
                    else:
                        label = labels.pop(0)
                        keys[key] = label
                    portals[free] = label
                    maze2[free[0]][free[1]] = label
                    maze2[i][j] = '#'
                    maze2[second[0]][second[1]] = '#'
    keys['.'] = '.'
    return maze2, expected, {v:k for k, v in keys.items()}


def makekey(maze, i, j, i2, j2):
    if (i, j) < (i2, j2):
        return maze[i][j] + maze[i2][j2]
    else:
        return maze[i2][j2] + maze[i][j]


def fill_dead_ends(maze):
    """
    save time by erasing dead ends
    """
    bouche = 1
    while bouche:
        bouche = 0
        for i, line in enumerate(maze[1:-1], 1):
            for j, char in enumerate(line[1:-1], 1):
                if char == '.':
                    nbwall = sum(maze[i + DELTA_I[d]][j + DELTA_J[d]] == '#' for d in range(4))
                    if nbwall >= 3:
                        maze[i][j] = '#'
                        bouche = 1
    return maze


def find_nodes(maze):
    """
    nodes are position of robot, keys and doors, and intersections.
    """
    nodes = set()
    for i, line in enumerate(maze[1:-1], 1):
        for j, char in enumerate(line[1:-1], 1):
            if char == '#':
                pass
            elif char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz':
                nodes.add((i, j))
            else:
                neigh = [(i2, j2) for i2, j2 in neighbours(maze, i, j) if maze[i2][j2] != '#']
                if len(neigh) in (1, 3, 4):
                    nodes.add((i, j))
    return nodes


def find_edges(maze, nodes):
    """
    construct adjacency matrix
    """
    edges = defaultdict(lambda: defaultdict(lambda: 10 ** 6))
    for node in nodes:
        neigh = [(i2, j2) for i2, j2 in neighbours(maze, *node) if maze[i2][j2] not in ' #']
        for pos in neigh:
            i2, j2, dist = follow_edge(maze, nodes, *node, *pos)
            edges[node][(i2, j2)] = dist
    return edges


def follow_edge(maze, nodes, i0, j0, i, j):
    visited = set()
    visited.add((i0, j0))
    dist = 1  # count from origin node
    while (i, j) not in nodes:
        visited.add((i, j))
        neigh = [(i2, j2) for i2, j2 in neighbours(maze, i, j) if (i2, j2) not in visited and maze[i2][j2] not in ' #']
        i, j = neigh[0]
        dist += 1
    return i, j, dist


def add_portal_edges(maze, edges):
    portals = dict()
    for i, line in enumerate(maze[2:-2], 2):
        for j, char in enumerate(line[2:-2], 2):
            if char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz':
                if maze[i][j] in portals:
                    edges[(i, j)][portals[maze[i][j]]] = 1
                    edges[portals[maze[i][j]]][(i, j)] = 1
                else:
                    portals[maze[i][j]] = (i, j)


def add_portal_edges2(maze, edges, maxlevel=10):
    #  char_to_coords[char] = pair of intersections
    char_to_coords = defaultdict(list)
    for i, line in enumerate(maze[2:-2], 2):
        for j, char in enumerate(line[2:-2], 2):
            if char in 'BCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxy':
                char_to_coords[char].append((i, j))

    # portals[inner] = outer
    portals = dict()
    for (i, j), (i2, j2) in char_to_coords.values():
        if i == 2 or i == len(maze) - 3 or j == 2 or j == len(maze[0]) - 3:
            portals[(i2, j2)] = (i, j)
        else:
            portals[(i, j)] = (i2, j2)

    # add levels to edges
    edges2 = defaultdict(lambda: defaultdict(lambda: 10 ** 6))
    for level in range(0, maxlevel + 1):
        for node_from in edges:
            if level == 0 or node_from not in ((34, 15), (2, 13)):
                for node_to in edges[node_from]:
                    if level == 0 or node_to not in ((34, 15), (2, 13)):
                        edges2[(level, *list(node_from))][(level, *list(node_to))] = edges[node_from][node_to]
        for inner, outer in portals.items():
            if level < maxlevel:
                edges2[(level, *list(inner))][(level + 1, *list(outer))] = 1
            if level > 0:
                edges2[(level, *list(outer))][(level - 1, *list(inner))] = 1

    return edges2


def transitive_closure(edges):
    # not used, keep for reference
    """
    compute distances between all pairs of node
    """
    distances = copy.deepcopy(edges)
    for node in distances:
        for node_from in distances:
            for node_to in distances:
                distances[node_from][node_to] = min(distances[node_from][node_to],
                                                    distances[node_from][node] + distances[node][node_to])
    return distances


def dijkstra(edges, start, end):
    dist = dict()
    for node in edges:
        dist[node] = float('inf')
    dist[start] = 0

    nodes = set(edges)
    while nodes:
        node = find_closest(nodes, dist)
        if node is None:
            nodes.clear()
        else:
            nodes.remove(node)
            for node2 in edges[node]:
                newdist = dist[node] + edges[node][node2]
                if newdist < dist[node2]:
                    dist[node2] = newdist

    return dist[end]


def find_closest(nodes, dist):
    mini = float('inf')
    xnode = None
    for node in nodes:
        if dist[node] < mini:
            mini = dist[node]
            xnode = node
    return xnode


def find_target(maze, target):
    """
    find first intersection in grid equal to target
    """
    for i, line in enumerate(maze[2:-2], 2):
        for j, char in enumerate(line[2:-2], 2):
            if char == target:
                return i, j
    return None


def code1(exemple):
    maze, expected, revkeys = makemaze(exemple)
    maze = fill_dead_ends(maze)
    for line in maze:
        print(''.join(line))
    nodes = find_nodes(maze)
    edges = find_edges(maze, nodes)
    add_portal_edges(maze, edges)
    start = find_target(maze, 'A')
    exitm = find_target(maze, 'z')
    distance = dijkstra(edges, start, exitm)
    print('1>', distance)
    if expected:
        assert expected == distance, (expected, distance)


def code2(exemple):
    maze, expected, revkeys = makemaze(exemple)
    maze = fill_dead_ends(maze)
    for line in maze:
        print(''.join(line))
    nodes = find_nodes(maze)
    edges = find_edges(maze, nodes)
    edges = add_portal_edges2(maze, edges, maxlevel=25)
    start = (0, *find_target(maze, 'A'))
    exitm = (0, *find_target(maze, 'z'))
    distance = dijkstra(edges, start, exitm)
    print('2>', distance)
    if expected:
        assert expected == distance, (expected, distance)


code1(1)
code1(2)
code1(0)
code2(3)
code2(4)
code2(0)
