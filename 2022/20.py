"""
--- 2022 --- Day 20: Grove Positioning System ---

Keywords: linked list
"""


EXAMPLES1 = (
    ('20-exemple1.txt', 3),
    ('20-exemple2.txt', None),
)

EXAMPLES2 = (
    ('20-exemple1.txt', 1623178306),
)

INPUT = '20.txt'


class Node:
    """
    Linked list
    """
    def __init__(self, value):
        self.value = value
        self.prev = self
        self.next = self

    def __str__(self):
        prev = 'None' if self.prev is None else self.prev.value
        next = 'None' if self.next is None else self.next.value
        return f'{self.value} <{prev} >{next}'

    def link(self, next):
        self.next = next
        next.prev = self

    def neighbour(self, offset):
        """
        node.neighbour(0)   = node
        node.neighbour(1)   = node.next
        node.neighbour(2)   = node.next.next
        node.neighbour(-1)   = node.prev
        node.neighbour(-2)   = node.prev.prev
        """
        target = self
        if offset >= 0:
            for _ in range(offset):
                target = target.next
        else:
            for _ in range(abs(offset)):
                target = target.prev
        return target

    def insertnode(self, offset, node):
        """
        Insert value just after node.neighbour(offset)
        node.insert(1, 42)  insert value 42 between node and node.next
        node.insert(0, 42)  insert value 42 between node and node.prev
        node.insert(-1, 42) insert value 42 just before node.prev
        Return inserted node
        """
        target = self.neighbour(offset)
        target.prev.link(node)
        node.link(target)
        return node

    def insert(self, offset, value):
        """
        Insert value just after node.neighbour(offset)
        node.insert(1, 42)  insert value 42 between node and node.next
        node.insert(0, 42)  insert value 42 between node and node.prev
        node.insert(-1, 42) insert value 42 just before node.prev
        Return inserted node
        """
        return self.insertnode(offset, Node(value))

    def remove(self, offset):
        """
        Return remove node and node next to it
        """
        target = self.neighbour(offset)
        target.prev.link(target.next)
        return target, target.next

    def length(self):
        n = 1
        node = self.next
        while node != self:
            n += 1
            node = node.next
        return n


    def printall(self):
        values = [self.value]
        node = self.next
        while node != self:
            values.append(node.value)
            node = node.next
        return ' '.join([str(_) for _ in values])


def read_data(filename):
    with open(filename) as f:
        data = [int(_) for _ in f.readlines()]

    pointers = []
    node = Node(data[0])
    pointers.append(node)
    for value in data[1:]:
        node = node.insert(1, value)
        pointers.append(node)

    return pointers


def code1(pointers):
    length = pointers[0].length()

    for node in pointers:
        value = node.value
        if value != 0:
            node0, node = node.remove(0)
            node.insertnode(value % (length - 1), node0)

    node = next(node for node in pointers if node.value == 0)

    return node.neighbour(1000).value + node.neighbour(2000).value + node.neighbour(3000).value


def code2(pointers):
    length = pointers[0].length()
    for node in pointers:
        node.value *= 811589153

    for _ in range(10):
        for node in pointers:
            value = node.value
            if value != 0:
                node0, node = node.remove(0)
                node.insertnode(value % (length - 1), node0)

    node = next(node for node in pointers if node.value == 0)

    return node.neighbour(1000).value + node.neighbour(2000).value + node.neighbour(3000).value


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


if __name__ == '__main__':
    test(1, code1, EXAMPLES1, INPUT)
    test(2, code2, EXAMPLES2, INPUT)
