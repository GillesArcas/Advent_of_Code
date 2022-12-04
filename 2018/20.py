"""
--- Day 20: A Regular Map ---

Keywords: parentheses, dijkstra
"""


import re
import itertools
from collections import defaultdict


EXAMPLES1 = (
    ('^WNE$', 3),
    ('^ENWWW(NEEE|SSE(EE|N))$', 10),
    ('^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$', 18),
    ('^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$', 23),
    ('^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$', 31),
)

EXAMPLES2 = (
)

INPUT = '20.txt'


def read_data(data):
    if data.startswith('^'):
        regex = data
    else:
        with open(data) as f:
            regex = f.read().strip()

    # get rid of ^$
    regex = regex[1:-1]
    # tokenize
    tokens = re.split(r'(\W)', regex)
    # remove useless empty strings
    tokens = [_ for i, _ in enumerate(tokens) if tokens[i - 1] == '|' or _ != '']

    regex = parse_parentheses(tokens)
    regex = prefix_or(regex)
    return regex


def push(obj, groups, depth):
    while depth:
        groups = groups[-1]
        depth -= 1
    groups.append(obj)


def parse_parentheses(tokens):
    # https://stackoverflow.com/a/50702934/380018
    groups = []
    depth = 0

    try:
        for token in tokens:
            if token == '(':
                push([], groups, depth)
                depth += 1
            elif token == ')':
                depth -= 1
            else:
                push(token, groups, depth)
    except IndexError:
        raise ValueError('Parentheses mismatch')

    if depth > 0:
        raise ValueError('Parentheses mismatch')
    else:
        return groups


def prefix_or(x):
    if isinstance(x, str):
        return x
    else:
        if '|' in x:
            return ['|'] + [prefix_or(list(y)) for x2, y in itertools.groupby(x, lambda z: z == '|')  if not x2]
        else:
            return [prefix_or(_) for _ in x]


def grid_bounds(grid):
    imin = min(grid)
    imax = max(grid)
    jmin, jmax = float('inf'), float('-inf')
    for i in range(imin, imax + 1):
        jmin = min(jmin, *grid[i])
        jmax = max(jmax, *grid[i])
    return imin, imax, jmin, jmax


def print_grid(grid):
    imin, imax, jmin, jmax = grid_bounds(grid)
    for i in range(imin, imax + 1):
        print(''.join([grid[i][j] for j in range(jmin, jmax + 1)]))
    print()


def explore_grid(regex):
    grid = defaultdict(lambda: defaultdict(lambda: '#'))
    grid[0][0] = 'X'
    explore(0, 0, grid, regex)

    # make sure grid[i][j] is defined (defaultgrid ...) and get rid of question marks
    imin, imax, jmin, jmax = grid_bounds(grid)
    for i in range(imin, imax + 1):
        for j in range(jmin, jmax + 1):
            if grid[i][j] == '?':
                grid[i][j] = '#'
    return grid


def explore(i, j, grid, regex):
    if isinstance(regex, str):
        for direction in regex:
            if direction == 'N':
                i -= 2
                grid[i][j] = '.'
                set_unknown(i, j, grid)
                grid[i + 1][j] = '-'
            elif direction == 'S':
                i += 2
                grid[i][j] = '.'
                set_unknown(i, j, grid)
                grid[i - 1][j] = '-'
            elif direction == 'W':
                j -= 2
                grid[i][j] = '.'
                set_unknown(i, j, grid)
                grid[i][j + 1] = '|'
            elif direction == 'E':
                j += 2
                grid[i][j] = '.'
                set_unknown(i, j, grid)
                grid[i][j - 1] = '|'
        return i, j
    else:
        if regex[0] == '|':
            i0, j0 = i, j
            for rx in regex[1:]:
                i, j = explore(i0, j0, grid, rx)
            return i, j
        else:
            for rx in regex:
                i, j = explore(i, j, grid, rx)
            return i, j


def set_unknown(i, j, grid):
    for i2, j2 in ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)):
        if grid[i2][j2] == '#':
            grid[i2][j2] = '?'


def grid_to_graph(grid):
    grid = dict(grid)
    graph = defaultdict(list)
    for i, line in grid.items():
        for j, val in line.items():
            if val in '.X':
                if grid[i - 1][j] == '-':
                    graph[(i, j)].append((i - 2, j))
                if grid[i + 1][j] == '-':
                    graph[(i, j)].append((i + 2, j))
                if grid[i][j - 1] == '|':
                    graph[(i, j)].append((i, j - 2))
                if grid[i][j + 1] == '|':
                    graph[(i, j)].append((i, j + 2))
    return graph


def dijkstra(edges, start):
    dist = {}
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
                newdist = dist[node] + 1  # edges[node][node2]
                if newdist < dist[node2]:
                    dist[node2] = newdist

    return dist


def find_closest(nodes, dist):
    mini = float('inf')
    xnode = None
    for node in nodes:
        if dist[node] < mini:
            mini = dist[node]
            xnode = node
    return xnode


def code1(regex):
    grid = explore_grid(regex)
    # print_grid(grid)
    graph = grid_to_graph(grid)
    dist = dijkstra(graph, (0, 0))
    return max(dist.values())


def code2(regex):
    grid = explore_grid(regex)
    graph = grid_to_graph(grid)
    dist = dijkstra(graph, (0, 0))
    count = sum(_ >= 1000 for _ in dist.values())
    return count


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
