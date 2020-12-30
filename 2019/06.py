DATA = '06.txt'
#DATA = '06-exemple1.txt'


class Node:
    def __init__(self, name):
        self.name = name
        self.height = 0
        self.sat = []
        self.main = None


def read_data(data):
    with open(data) as f:
        spec = [line.strip().split(')') for line in f.readlines()]
    return load_data(spec)


def load_data(data):
    allnodes = dict()
    for main, sat in data:
        if main not in allnodes:
            allnodes[main] = Node(main)
        if sat not in allnodes:
            allnodes[sat] = Node(sat)
    for main, sat in data:
        allnodes[main].sat.append(allnodes[sat])
        allnodes[sat].main = allnodes[main]
    return allnodes


def set_height(node, height):
    node.height = height
    for sat in node.sat:
        set_height(sat, height + 1)


def predecessors(node):
    pred = node.main
    allpred = [pred]
    while pred.main:
        pred = pred.main
        allpred.append(pred)
    return allpred


def code1():
    allnodes = read_data(DATA)
    set_height(allnodes['COM'], 0)
    print('1>', sum(node.height for node in allnodes.values()))


def code2():
    allnodes = read_data(DATA)
    set_height(allnodes['COM'], 0)
    you_pred = predecessors(allnodes['YOU'])
    san_pred = predecessors(allnodes['SAN'])
    common = [node for node in you_pred if node in san_pred][0]
    print([node.name for node in you_pred])
    print([node.name for node in san_pred])
    print(common.name)
    print('2>', (allnodes['YOU'].main.height - common.height) + (allnodes['SAN'].main.height - common.height))


code1()
code2()
