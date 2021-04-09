import re


DATA = """\
     9 players; last marble is worth    25 points: high score is 32
    10 players; last marble is worth  1618 points: high score is 8317
    13 players; last marble is worth  7999 points: high score is 146373
    17 players; last marble is worth  1104 points: high score is 2764
    21 players; last marble is worth  6111 points: high score is 54718
    30 players; last marble is worth  5807 points: high score is 37305
   479 players; last marble is worth 71035 points: high score is 0
""".splitlines()


def read_data(n):
    line = DATA[n]
    match = re.search(r'(\d+) players; last marble is worth\s*(\d+) points: high score is (\d+)', line)
    players, last_marble, score = match.group(1, 2, 3)
    return int(players), int(last_marble), int(score)


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


def play(players, last_marble):
    scores = [0] * players
    player = 0
    current = Node(0)
    start = current
    current.link(current)

    for marble in range(1, last_marble + 1):
        player = (player + 1) % players
        if marble % 23 == 0:
            scores[player] += marble
            removed, current = current.remove(-7)
            scores[player] += removed.value
        else:
            current = current.insert(2, marble)

    return max(scores)


def code1():
    for _ in range(len(DATA)):
        players, last_marble, expected_score = read_data(_)
        score = play(players, last_marble)
        if expected_score:
            assert score == expected_score, (score, expected_score)
        else:
            print('1>', score)


def code2():
    players, last_marble, expected_score = read_data(len(DATA) - 1)
    score = play(players, last_marble * 100)
    print('2>', score)


code1()
code2()
