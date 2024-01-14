"""
--- Day 23: A Long Walk ---
"""


from functools import cache


EXAMPLES1 = (
    ('23-exemple1.txt', 94),
)

EXAMPLES2 = (
    ('23-exemple1.txt', 154),
)

INPUT = '23.txt'


def read_data(filename):
    with open(filename) as f:
        lines = [_.strip() for _ in f.readlines()]
    return lines


def grid_to_path(lines, mode):
    """
    mode=1 for part 1, 2 for part 2
    """
    normal = '.' if mode == 1 else '.<>^v'
    graph = {}
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == '#':
                pass
            elif char in normal:
                succ = {}
                for i2, j2 in ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)):
                    if 0 <= i2 < len(lines) and 0 <= j2 < len(line):
                        if lines[i2][j2] != '#':
                            succ[i2, j2] = 1
                graph[i, j] = succ
            elif char == '>':
                graph[i, j] = {(i, j + 1): 1}
            elif char == 'v':
                graph[i, j] = {(i + 1, j): 1}
            else:
                assert 0
    start = 0, 1
    end = len(lines) - 1, len(lines[0]) - 2

    return start, end, graph


def all_paths_v1(start, end, graph):
    stack = []
    stack.append([start])
    while stack:
        path = stack.pop()
        last = path[-1]
        if last == end:
            yield path
        else:
            for node in graph[last]:
                if node not in path:
                    stack.append(path + [node])


def all_paths_v2(start, end, graph):
    """
    push partial paths and corresponding sets for faster testing
    """
    stack = []
    stack.append(([start], set(start)))
    while stack:
        path, setpath = stack.pop()
        last = path[-1]
        if last == end:
            yield path
        else:
            for node in graph[last]:
                if node not in setpath:
                    stack.append((path + [node], setpath | {node}))


def all_paths(start, end, graph):
    """
    - cache paths in corridors with no crossing
    - 3 hours for part 2
    - next step should be to reduce the graph to a graaph with no corridors and
      weights equal to lengths
    """
    @cache
    def next_path(node, succ):
        if len(graph[node]) > 2:
            path = [succ]
        else:
            path = [succ]
            while len(graph[succ]) == 2:
                for succ2 in graph[succ]:
                    if succ2 != node:
                        path.append(succ2)
                        node = succ
                        succ = succ2
                        break
        return path, set(path)

    stack = []
    stack.append(([start], set(start)))
    while stack:
        path, setpath = stack.pop()
        last = path[-1]
        if last == end:
            yield path
        else:
            for node in graph[last]:
                p, s = next_path(last, node)
                # print(p)
                if p[-1] not in setpath:
                    stack.append((path + p, setpath | s))


def code(lines, mode):
    start, end, graph = grid_to_path(lines, mode=mode)
    res = 0
    for path in all_paths(start, end, graph):
        lenpath = len(path) - 1
        if lenpath > res:
            res = lenpath
            print(res)
    return res


def code1(lines):
    return code(lines, mode=1)


def code2(lines):
    # 6686 too high
    # 6685 too high
    return code(lines, mode=2)


def test(n, code, examples, myinput):
    for fn, expected in examples:
        print(fn)
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
