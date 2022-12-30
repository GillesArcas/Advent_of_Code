"""
--- 2022 --- Day 16: Proboscidea Volcanium ---

Keywords: Floyd-Warshall, fermeture transitive
"""


import re


EXAMPLES1 = (
    ('16-exemple1.txt', 1651),
)

EXAMPLES2 = (
)

INPUT = '16.txt'


PAT = r'Valve ([A-Z]+) has flow rate=(\d+); tunnels? leads? to valves? ([A-Z, ]+)'


class Valve:
    def __init__(self, name=None, flow=None, nextvalves=None):
        self.name = name
        self.visited = 0
        self.isopen = False
        self.flow = flow
        self.nextvalves = nextvalves
        self.timesofar = None
        self.pressuresofar = None
        self.path = []
        self.closed_valves = set()

    def __str__(self):
        return 'Valve: ' + self.name

    def copy(self, other):
        self.name = other.name
        self.visited = other.visited
        self.isopen = other.isopen
        self.flow = other.flow
        self.nextvalves = other.nextvalves
        self.timesofar = other.timesofar
        self.pressuresofar = other.pressuresofar
        self.path = other.path.copy()
        self.closed_valves = other.closed_valves.copy()
        return self


def read_data(filename):
    with open(filename) as f:
        data = f.read()
    valves = {}
    for name, flow, names in re.findall(PAT, data):
        valves[name] = Valve(name, int(flow), names.split(', '))
    return valves


INF = 1_000_000


def transitive_closure(valves):
    """
    compute distances between all pairs of valves
    """
    distances = {}
    for name1 in valves:
        distances[name1] = {}
        for name2 in valves:
            distances[name1][name2] = INF

    for name1, valve1 in valves.items():
        for name2 in valve1.nextvalves:
            distances[name1][name2] = 1

    for node in distances:
        for node_from in distances:
            for node_to in distances:
                distances[node_from][node_to] = min(distances[node_from][node_to],
                                                    distances[node_from][node] + distances[node][node_to])

    nonzero_valves = set()
    nonzero_valves.add('AA')
    for name, valve in valves.items():
        if valve.flow > 0:
            nonzero_valves.add(name)

    distances2 = {}
    for valve1 in sorted(nonzero_valves):
        distances2[valve1] = {}
        for valve2 in sorted(nonzero_valves):
            if valve2 != valve1:
                distances2[valve1][valve2] = distances[valve1][valve2]

    return distances2


def genpaths(closed, distances, maxdist):
    stack = []
    for x in closed:
        path = [x]
        rest = closed.copy()
        rest.remove(x)
        stack.append((x, path, rest, distances['AA'][x]))

    while stack:
        x, path, closed, distance = stack.pop(0)
        yield x, path, distance
        for y in closed:
            dist = distance + distances[x][y] + 1   # +1 pour ouverture
            if dist <= maxdist:
                rest = closed.copy()
                rest.remove(y)
                stack.append((y, path + [y], rest, dist))

    yield None, None, None


def path_pressure(path, distances, valves, maxdist):
    v1 = 'AA'
    t = 0
    pressure = 0
    for v2 in path:
        t += distances[v1][v2] + 1
        pressure += (maxdist - t) * valves[v2].flow
        v1 = v2
    return pressure


def code1(valves):
    distances = transitive_closure(valves)
    nonzero_valves = set()
    for name, valve in valves.items():
        if valve.flow > 0:
            nonzero_valves.add(name)
    paths = genpaths(nonzero_valves, distances, maxdist=30)
    n = 0
    maxpressure = 0
    while True:
        x, path, dist = next(paths)
        if x:
            n += 1
            pressure = path_pressure(path, distances, valves, maxdist=30)
            if pressure > maxpressure:
                maxpressure = pressure
                maxpath = path
        else:
            print('=', n, maxpath)
            break

    return maxpressure


def code2(valves):
    distances = transitive_closure(valves)
    nonzero_valves = set()
    for name, valve in valves.items():
        if valve.flow > 0:
            nonzero_valves.add(name)

    paths = genpaths(nonzero_valves, distances, maxdist=26)
    maxpressure = 0
    while True:
        x, path, dist = next(paths)
        if x:
            pressure = path_pressure(path, distances, valves, maxdist=26)
            paths_eleph = genpaths(nonzero_valves.difference(set(path)), distances, maxdist=26)
            print(nonzero_valves.difference(set(path)))
            while True:
                x2, path2, dist2 = next(paths_eleph)
                if x2:
                    pressure2 = path_pressure(path2, distances, valves, maxdist=26)

                    if pressure + pressure2 > maxpressure:
                        maxpressure = pressure + pressure2
                else:
                    break
        else:
            break

    return maxpressure


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


# test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
