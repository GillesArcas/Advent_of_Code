import copy
from collections import defaultdict
from colorama import Fore, Style


DELTA_I = (0, -1, 0, 1)
DELTA_J = (1, 0, -1, 0)


def getdata(part, n):
    if part == 1:
        if n == 0:
            filename = '18.txt'
            result = None
        elif n == 1:
            filename = '18-exemple1.txt'
            result = 8
        elif n == 2:
            filename = '18-exemple2.txt'
            result = 86
        elif n == 3:
            filename = '18-exemple3.txt'
            result = 132
        elif n == 4:
            filename = '18-exemple4.txt'
            result = 136
        elif n == 5:
            filename = '18-exemple5.txt'
            result = 81
        else:
            assert 0
    else:
        if n == 0:
            filename = '18-2.txt'
            result = None
        elif n == 1:
            filename = '18-2-exemple1.txt'
            result = 8
        elif n == 2:
            filename = '18-2-exemple2.txt'
            result = 24
        elif n == 3:
            filename = '18-2-exemple3.txt'
            result = 32
        elif n == 4:
            filename = '18-2-exemple4.txt'
            result = 72
        else:
            assert 0

    with open(filename) as f:
        lines = [line.strip() for line in f.readlines()]
    data = [list(line) for line in lines]
    return data, result


def fill_dead_ends(data):
    """
    save time by erasing dead ends without keys or doors (ratio about 40s to 5s)
    """
    bouche = 1
    while bouche:
        bouche = 0
        for i, line in enumerate(data[1:-1], 1):
            for j, char in enumerate(line[1:-1], 1):
                if char == '.':
                    nbwall = sum(data[i + DELTA_I[d]][j + DELTA_J[d]] == '#' for d in range(4))
                    if nbwall >= 3:
                        data[i][j] = '#'
                        bouche = 1
    return data


def find_target(data, target):
    """
    find first intersection in grid equal to target
    """
    for i, line in enumerate(data[1:-1], 1):
        for j, char in enumerate(line[1:-1], 1):
            if char == target:
                return i, j


def find_targets(data, target):
    """
    find all intersections in grid equal to target
    """
    targets = list()
    for i, line in enumerate(data[1:-1], 1):
        for j, char in enumerate(line[1:-1], 1):
            if char == target:
                targets.append((i, j))
    return targets


def count_keys(data):
    return sum(sum(char in 'abcdefghijklmnopqrstuvwxyz' for char in line) for line in data)


def neighbours(i, j):
    return (i, j + 1), (i - 1, j), (i, j - 1), (i + 1, j)


def find_nodes(data):
    """
    nodes are position of robot, keys and doors, and intersections.
    """
    nodes = set()
    for i, line in enumerate(data[1:-1], 1):
        for j, char in enumerate(line[1:-1], 1):
            if char == '#':
                pass
            elif char != '.':
                nodes.add((i, j))
            else:
                neigh = [(i2, j2) for i2, j2 in neighbours(i, j) if data[i2][j2] != '#']
                if len(neigh) in (1, 3, 4):
                    nodes.add((i, j))
    return nodes


def find_edges(data, nodes, edges):
    """
    construct adjacency matrix
    """
    for node in nodes:
        neigh = [(i2, j2) for i2, j2 in neighbours(*node) if data[i2][j2] != '#']
        for pos in neigh:
            i2, j2, dist = follow_edge(data, nodes, *node, *pos)
            edges[node][(i2, j2)] = dist


def follow_edge(data, nodes, i0, j0, i, j):
    visited = set()
    visited.add((i0, j0))
    dist = 1  # count from origin node
    while (i, j) not in nodes:
        visited.add((i, j))
        neigh = [(i2, j2) for i2, j2 in neighbours(i, j) if (i2, j2) not in visited and data[i2][j2] != '#']
        i, j = neigh[0]
        dist += 1
    return i, j, dist


def transitive_closure(edges):
    """
    compute distances between all pairs of node
    """
    distances = copy.deepcopy(edges)
    proceed = True
    while proceed:
        proceed = False
        distances2 = copy.deepcopy(distances)
        for node_from, nodes_to in distances.items():
            for node_to, distance in nodes_to.items():
                for node_to2, distance2 in edges[node_to].items():
                    if node_to2 not in distances[node_from] and node_to2 != node_from:
                        distances2[node_from][node_to2] = distance + distance2
                        proceed = True
        distances = copy.deepcopy(distances2)
    return distances


def accessible_keys(data, nodes, edges, start, visited, excepted=None):
    """
    find all keys directly accessible from start
    """
    visited.add(start)
    found = set()
    nodes2 = edges[start].keys()

    for node in nodes2:
        if node == excepted:
            pass
        elif node in visited:
            pass
        elif data[node[0]][node[1]] in 'abcdefghijklmnopqrstuvwxyz':
            found.add(node)
        elif data[node[0]][node[1]] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            pass
        elif 0 and data[node[0]][node[1]][0] == '-':
            pass
        else:
            found = found.union(accessible_keys(data, nodes, edges, node, visited, excepted=start))
    return found


def search(data, nodes, edges, distances, nbkeys, cache, foundkeys, robot, currdist):
    # all keys have been found ?
    if len(foundkeys) == nbkeys:
        return currdist

    # couple (robot node, found keys) already in cache
    foundk = ''.join(sorted(foundkeys))
    if (robot, foundk) in cache:
        return currdist + cache[(robot, foundk)]

    # no accessible keys
    keynodes = accessible_keys(data, nodes, edges, robot, visited=set())
    if not keynodes:
        return float('inf')

    # search min for all accessible keys
    mincost = float('inf')
    for node in keynodes:
        key = data[node[0]][node[1]]
        door = key.upper()
        foundkeys.append(key)

        # mark key and associated door
        data[node[0]][node[1]] = '-' + key
        posdoor = find_target(data, door)
        if posdoor:
            idoor, jdoor = posdoor
            data[idoor][jdoor] = '-' + door

        cost = search(data, nodes, edges, distances, nbkeys, cache, foundkeys, node, currdist + distances[robot][node])
        if cost < mincost:
            mincost = cost

        # unmark
        data[node[0]][node[1]] = key
        if posdoor:
            data[idoor][jdoor] = door

        foundkeys.pop()

    cache[(robot, foundk)] = mincost - currdist
    return mincost


def search2(data, nodes, edges, distances, nbkeys, cache, foundkeys, robots, currdist):
    # all keys have been found ?
    if len(foundkeys) == nbkeys:
        return currdist

    # couple (list of robot nodes, found keys) already in cache
    foundk = ''.join(sorted(foundkeys))
    if (tuple(robots), foundk) in cache:
        return currdist + cache[(tuple(robots), foundk)]

    # search min for all accessible keys
    mincost = float('inf')
    for numrobot, robot in enumerate(robots):
        # no accessible keys
        keynodes = accessible_keys(data, nodes, edges, robot, visited=set())
        if not keynodes:
            cost = float('inf')
            continue

        for node in keynodes:
            robots[numrobot] = node

            key = data[node[0]][node[1]]
            door = key.upper()
            foundkeys.append(key)

            # mark key and associated door
            data[node[0]][node[1]] = '-' + key
            posdoor = find_target(data, door)
            if posdoor:
                idoor, jdoor = posdoor
                data[idoor][jdoor] = '-' + door

            cost = search2(data, nodes, edges, distances, nbkeys, cache, foundkeys, robots, currdist + distances[robot][node])
            if cost < mincost:
                mincost = cost

            # unmark
            data[node[0]][node[1]] = key
            if posdoor:
                data[idoor][jdoor] = door

            foundkeys.pop()

        # restore robot
        robots[numrobot] = robot

    cache[(tuple(robots), foundk)] = mincost - currdist
    return mincost


def code1(exemple):
    data, expected = getdata(1, exemple)
    data = fill_dead_ends(data)
    robot = find_target(data, '@')
    nodes = find_nodes(data)
    edges = defaultdict(lambda: defaultdict(int))
    find_edges(data, nodes, edges)
    for line in data:
        print(''.join(line))

    distances = transitive_closure(edges)
    cache = dict()
    foundkeys = list()
    currdist = 0
    mindist = search(data, nodes, edges, distances, count_keys(data), cache, foundkeys, robot, currdist)
    print('1>', mindist)
    if expected:
        assert expected == mindist


def code2(exemple):
    data, expected = getdata(2, exemple)
    data = fill_dead_ends(data)
    robots = find_targets(data, '@')
    nodes = find_nodes(data)
    edges = defaultdict(lambda: defaultdict(int))
    find_edges(data, nodes, edges)
    for line in data:
        print(''.join(line))

    distances = transitive_closure(edges)
    cache = dict()
    foundkeys = list()
    currdist = 0
    mindist = search2(data, nodes, edges, distances, count_keys(data), cache, foundkeys, robots, currdist)
    print('2>', mindist)
    if expected:
        assert expected == mindist


# code1(1)
# code1(2)
# code1(3)
# code1(4)
# code1(5)
# code1(0)
code2(1)
code2(2)
code2(3)
code2(4)
code2(0)
