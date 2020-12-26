EXEMPLE = 0
if EXEMPLE == 0:
    DATA = '739862541'
    NBMOVES = 100
elif EXEMPLE == 1:
    DATA = '389125467'
    NBMOVES = 10
elif EXEMPLE == 2:
    DATA = '389125467'
    NBMOVES = 100
else:
    assert False


class Node:
    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None

    def link(self, next):
        self.next = next
        next.prev = self

    def printall(self):
        values = [self.value]
        nextnode = self.next
        while nextnode.value != self.value:
            values.append(nextnode.value)
            nextnode = nextnode.next
        return values


def run(values, nbmoves):
    trace = 0
    max_cup = max(values)
    nodes = [Node(x) for x in values]
    value_to_nodes = {node.value: node for node in nodes}
    for index, node in enumerate(nodes[:-1]):
        node.link(nodes[index + 1])
    nodes[-1].link(nodes[0])

    current_node = nodes[0]
    for _ in range(nbmoves):
        if trace: print('cups:', current_node.printall())
        if trace: print('current_cup:', current_node.value)
        pick_nodes = [current_node.next, current_node.next.next, current_node.next.next.next]
        pick_cups = [node.value for node in pick_nodes]
        if trace: print('picked_cups:', pick_cups)

        current_node.link(pick_nodes[2].next)

        dest_cup = current_node.value
        while 1:
            dest_cup -= 1
            if dest_cup == 0:
                dest_cup = max_cup
            if dest_cup not in pick_cups:
                break

        dest_node = value_to_nodes[dest_cup]
        if trace: print('dest:', dest_node.value)

        next_node = dest_node.next
        dest_node.link(pick_nodes[0])
        pick_nodes[2].link(next_node)

        current_node = current_node.next
        if trace: print()
    return value_to_nodes


def go1(data, nbmoves):
    values = [int(x) for x in data]
    value_to_nodes = run(values, nbmoves)
    node = value_to_nodes[1]
    print('cups:', node.printall())
    print('1>', ''.join([str(_) for _ in node.printall()[1:]]))


def go2(data, nbmoves):
    values = [int(x) for x in data] + list(range(10, 1_000_000 + 1))
    value_to_nodes = run(values, nbmoves)
    node = value_to_nodes[1]
    cup1 = node.next.value
    cup2 = node.next.next.value
    print('2>', cup1, cup2, cup1 * cup2)


def code1():
    go1(DATA, NBMOVES)


def code2():
    go2(DATA, 10_000_000)


code1()
code2()
