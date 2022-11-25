import re


EXAMPLES1 = (
    (3, 638),
)

EXAMPLES2 = (
)

INPUT = 324


def read_data(data):
    return data


class Node:
    """
    Circular list
    """
    def __init__(self, value):
        self.value = value
        self.prev = self
        self.next = self

    def __str__(self):
        return f'{self.value} <{self.prev.value} >{self.next.value}'

    def link(self, next):
        self.next = next
        next.prev = self

    def neighbour(self, offset):
        target= self
        if offset >= 0:
            for _ in range(offset):
                target = target.next
        else:
            for _ in range(abs(offset)):
                target = target.prev
        return target

    def insert(self, offset, value):
        """
        Return inserted node
        """
        node = Node(value)
        target = self.neighbour(offset)
        target.prev.link(node)
        node.link(target)
        return node

    def remove(self, offset):
        """
        Return remove node and node right to it
        """
        target = self.neighbour(offset)
        target.prev.link(target.next)
        return target, target.next

    def printall(self):
        values = [self.value]
        nextnode = self.next
        while nextnode.value != self.value:
            values.append(nextnode.value)
            nextnode = nextnode.next
        return ' '.join([str(_) for _ in values])


def code1(data):
    steps = data
    buffer = Node(0)
    ptr = buffer
    for n in range(1, 2017 + 1):
        ptr = ptr.insert(steps+1, n)
    return ptr.neighbour(1).value


def code2(data):
    steps = data
    buffer = Node(0)
    ptr = buffer
    for n in range(1, 50000000 + 1):
        if n % 1000000 == 0:
            print(n)
        ptr = ptr.insert(steps+1, n)
    return buffer.neighbour(1).value


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
