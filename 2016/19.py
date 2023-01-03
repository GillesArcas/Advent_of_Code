"""
--- 2016 --- Day 19: An Elephant Named Joseph ---
"""


EXAMPLES1 = (
    ('19-exemple1.txt', 3),
)

EXAMPLES2 = (
    # ('19-exemple1.txt', 2),
)

INPUT = '19.txt'


def read_data(filename):
    with open(filename) as f:
        return int(f.read())


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


def code1(nb):
    root = Node([1, 1])
    node = root
    for num in range(2, nb + 1):
        node = node.insert(1, [num, 1])

    node = root
    while node.value[1] < nb:
        node.value[1] += node.next.value[1]
        _, node = node.remove(1)
    return node.value[0]


def code2_naive(nb):
    root = Node([1, 1])
    node = root
    for num in range(2, nb + 1):
        node = node.insert(1, [num, 1])

    node = root
    length = nb
    while node.value[1] < nb:
        removed, _ = node.remove(length // 2)
        node.value[1] += removed.value[1]
        node = node.next
        length -= 1
    return node.value[0]


def code2(nb):
    """
    When tracing code2_naive(i) for i in range(2, xx), we get returning values equal to 1
    for i == 2, 10, 28, 82, ... ie i = 3 * n - 2. From 3 * n - 2 <= i <= 2 * n - 2,
    return values increase with step 1, and above, return values increase by step 2
    leading to the formulas.
    """
    n = 2
    while 3 * n - 2 <= nb:
        n = 3 * n - 2
    if nb <= 2 * n - 2:
        return nb - n + 1
    else:
        return n - 1 + 2 * (nb - 2 * n + 2)


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


for i in range(2, 101):
    assert code2_naive(i) == code2(i)
    
test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
