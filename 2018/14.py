import itertools


class Node:
    """
    Linked list
    """
    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None

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
        node.insert(1, 42)  insert value 42 just after a
        node.insert(0, 42)  insert value 42 just before a
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


def step(start, elf1, elf2, length):
    new = elf1.value + elf2.value
    if new < 10:
        start.insert(0, new)
        length += 1
    else:
        start.insert(0, new // 10)
        start.insert(0, new % 10)
        length += 2
    elf1 = elf1.neighbour(1 + elf1.value)
    elf2 = elf2.neighbour(1 + elf2.value)
    return elf1, elf2, length


def run1(count):
    start = Node(3)
    start.link(start)
    start.insert(0, 7)
    length = 2
    elf1 = start
    elf2 = start.next
    for _ in range(count + 10 - 2):
        elf1, elf2, length = step(start, elf1, elf2, length)

    scores = list()
    node = start.neighbour(count)
    for _ in range(10):
        scores.append(node.value)
        node = node.neighbour(1)
    return ''.join(map(str, scores))


def run2(target):
    start = Node(3)
    start.link(start)
    start.insert(0, 7)
    length = 2
    elf1 = start
    elf2 = start.next
    for _ in range(len(target) - 2):
        elf1, elf2, length = step(start, elf1, elf2, length)

    scores = list()
    node = start
    for _ in range(len(target)):
        node = node.prev
        scores.insert(0, node.value)

    for _ in itertools.count():
        length0 = length
        elf1, elf2, length = step(start, elf1, elf2, length)
        if length - length0 == 1:
            scores.pop(0)
            scores.append(start.neighbour(-1).value)
            if ''.join(map(str, scores)) == target:
                return length - len(target)
        else:
            scores.pop(0)
            scores.append(start.neighbour(-2).value)
            if ''.join(map(str, scores)) == target:
                return length - 1 - len(target)
            scores.pop(0)
            scores.append(start.neighbour(-1).value)
            if ''.join(map(str, scores)) == target:
                return length - len(target)


def code1():
    assert run1(9) == '5158916779'
    assert run1(5) == '0124515891'
    assert run1(18) == '9251071085'
    assert run1(2018) == '5941429882'
    print('1>', run1(323081))


def code2():
    assert run2('01245') == 5
    assert run2('51589') == 9
    assert run2('92510') == 18
    assert run2('59414') == 2018
    print('2>', run2('323081'))


code1()
code2()
