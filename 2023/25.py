"""
--- Day 25: Snowverload ---

The algorithm tries to disconnect the graph by removing triplets of edges
chosen in a reduce set.
Initialize first the two components with `peripheral` nodes, ie nodes with distance
equal to the maximum distance in the graph (the diameter of the graph). After
that, neighbours of the nodes already in the components are added while there
is no overlap. Finally, the relevant set of edges is constructed as the set of
edges from nodes outside the two components.

This reduces the edges to consider to 108 (out of the 3320 of the full graph)
and execution time to 4.5 minutes.

The algorithm to find peripheral nodes (nodes farthest from the farthest nodes
from a random node) has been found in https://www.reddit.com/r/learnpython/comments/jpvsf9/networkx_graph_theory_finding_farthest_two_points/
without reference or justification.
"""


import re
import itertools
import heapq


EXAMPLES1 = (
    ('25-exemple1.txt', None),
)

EXAMPLES2 = (
)

INPUT = '25.txt'


def read_data(filename):
    graph = {}
    with open(filename) as f:
        for node, nodes in  re.findall(r'(\w+): (.*)', f.read()):
            if node not in graph:
                graph[node] = {}
            for succ in nodes.split():
                graph[node][succ] = 1
                if succ not in graph:
                    graph[succ] = {}
                graph[succ][node] = 1
    return graph


def graphviz_format(graph, fn):
    with open(fn, 'wt') as f:
        print('graph G {', file=f)
        for node, nodes in graph.items():
            print(node, '-- {', ' '.join(nodes.keys()), '};', file=f)
        print('}', file=f)


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

        if node not in graph:
            continue
        for node2 in graph[node]:
            newdist = cost_so_far[node] + graph[node][node2]
            if node2 not in cost_so_far or newdist < cost_so_far[node2]:
                cost_so_far[node2] = newdist
                came_from[node2] = node
                heapq.heappush(routes, (newdist, node2))

    return None, None, None


def distances_from_node(graph, start):
    stack = []
    distances = {}
    stack.append(start)
    for node in graph:
        distances[node] = float('inf')
    distances[start] = 0
    while stack:
        node = stack.pop()
        for succ in graph[node]:
            d = distances[node] + 1
            if d < distances[succ]:
                distances[succ] = d
                stack.append(succ)
    return distances


def add_neighbours(graph, core):
    core_ = core.copy()
    for node in core:
        core_.update(graph[node])
    return core_


def code1(graph):
    # find pairs of peripheral nodes (pairs of nodes as far as possible)
    # start with random node
    start = list(graph)[0]

    # find all nodes farthest from start
    dist = distances_from_node(graph, start)
    distmax = max(dist.values())
    farthest = [node for node, d in dist.items() if d == distmax]

    # find all nodes farthest from farthest
    diameter = 0
    peripheral = set()
    for node in farthest:
        dist = distances_from_node(graph, node)
        distmax = max(dist.values())
        if distmax > diameter:
            diameter = distmax
            peripheral = set()
        if distmax >= diameter:
            peripheral.update([tuple(sorted((node, n))) for n, d in dist.items() if d == distmax])
    print(diameter, peripheral)

    # very particular case, works because one of the core has only one elements
    core1 = {x for x, _ in peripheral}
    core2 = {y for _, y in peripheral}
    print(core1, core2)

    # increase cores and stop before they overlap
    while 1:
        core1_ = add_neighbours(graph, core1)
        core2_ = add_neighbours(graph, core2)
        if core1_.intersection(core2_) != set():
            break
        core1 = core1_
        core2 = core2_

    # set of nodes outside both cores
    between = set(graph).difference(core1).difference(core2)
    print(len(graph), len(core1), len(core2), len(between))
    print(between)

    # set of edges from between nodes, candidates for disconnecting edges
    between_edges = set()
    for node in between:
        between_edges.update([tuple(sorted((node, n))) for n in graph[node]])
    print(len(between_edges), 'out of', sum(len(_) for _ in graph.values()) // 2)

    # choose one random node from each core
    node1 = list(core1)[0]
    node2 = list(core2)[0]

    # test combinations of 3 candidate edges
    for index, edges in enumerate(itertools.combinations(between_edges, 3), 1):
        # print(index, edges)
        for edge in edges:
            del graph[edge[0]][edge[1]]
            del graph[edge[1]][edge[0]]

        dist, _, _ = dijkstra(graph, node1, node2)
        if dist is None:
            # break when disconnected
            break

        for edge in edges:
            graph[edge[0]][edge[1]] = 1
            graph[edge[1]][edge[0]] = 1

    # graph is disconnected, complete one of the cores
    component = core1
    while (component2 := add_neighbours(graph, component)) != component:
        component = component2

    print(len(component), len(graph) - len(component), len(component) * (len(graph) - len(component)))
    return len(component) * (len(graph) - len(component))


def code2(data):
    return


def test(n, code, examples, myinput):
    for fn, expected in examples:
        print(fn)
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
