"""Advent of code 2018-15: Beverage Bandits

shortest path, dijkstra
"""
from collections import defaultdict


DATA0 = """\
################################
####.#######..G..########.....##
##...........G#..#######.......#
#...#...G.....#######..#......##
########.......######..##.E...##
########......G..####..###....##
#...###.#.....##..G##.....#...##
##....#.G#....####..##........##
##..#....#..#######...........##
#####...G.G..#######...G......##
#########.GG..G####...###......#
#########.G....EG.....###.....##
########......#####...##########
#########....#######..##########
#########G..#########.##########
#########...#########.##########
######...G..#########.##########
#G###......G#########.##########
#.##.....G..#########..#########
#............#######...#########
#...#.........#####....#########
#####.G..................#######
####.....................#######
####.........E..........########
#####..........E....E....#######
####....#.......#...#....#######
####.......##.....E.#E...#######
#####..E...####.......##########
########....###.E..E############
#########.....##################
#############.##################
################################
"""


DATA1 = """\
#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######
"""


DATA2 = """\
#######
#G..#E#
#E#E.E#
#G.##.#
#...#E#
#...E.#
#######
"""


DATA3 = """\
#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######
"""


DATA4 = """\
#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######
"""

DATA5 = """\
#######
#.E...#
#.#..G#
#.###.#
#E#G#G#
#...#G#
#######
"""


DATA6 = """\
#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########
"""


INF = float('inf')


class Node:
    ident = 0
    attack = 3
    def __init__(self, x, y, char):
        self.x = x
        self.y = y
        self.value = char
        self.attack = {'#': None, '.': None, 'G': 3, 'E': Node.attack}[char]
        self.hit_points = None if char in '#.' else 200
        self.neighbours = list()
        self.ident = Node.ident
        Node.ident += 1


def load_nodes(data):
    mat = defaultdict(lambda: defaultdict(Node))
    for y, line in enumerate(data.splitlines()):
        for x, char in enumerate(line):
            mat[y][x] = Node(x, y, char)
    for y in mat:
        for x in mat[y]:
            if mat[y][x].value != '#':
                for dy, dx in ((-1, 0), (0, -1), (0, 1), (1, 0)):
                    if mat[y + dy][x + dx].value != '#':
                        mat[y][x].neighbours.append(mat[y + dy][x + dx])
    return mat


def print_mat(mat):
    for line in mat.values():
        print(''.join(node.value for node in line.values()), end=' ')
        points = list()
        for node in line.values():
            if node.value in 'EG':
                points.append('%s(%s)' % (node.value, node.hit_points))
        print(' '.join(points))


def list_of_units(mat, kind):
    """
    return units in reading order
    """
    units = list()
    for y in mat:
        for x in mat[y]:
            if mat[y][x].value in kind:
                units.append(mat[y][x])
    return units


ENEMY = {'E': 'G', 'G': 'E'}


def enemies_in_contact(unit):
    """
    return neighbour enemies in reading order (as neighbours are)
    """
    in_contact = list()
    for neighbour in unit.neighbours:
        if neighbour.value == ENEMY[unit.value]:
            in_contact.append(neighbour)
    return in_contact


def chose_enemy(in_contact):
    return sorted(in_contact, key=lambda node: (node.hit_points, node.y, node.x))[0]


def get_in_range(enemies):
    """
    return list of intersections touching enemies (order irrelevant)
    """
    in_range = set()
    for enemy in enemies:
        for neighbour in enemy.neighbours:
            if neighbour.value == '.':
                in_range.add(neighbour)
    return in_range


def closest_in_range(mat, unit, in_range):
    """
    return closest in range intersection (reading order if tie)
    """
    dist = dijkstra(mat, unit)
    for inter in in_range:
        inter.distance = dist.get(inter.ident, INF)
    return sorted(in_range, key=lambda node: (node.distance, node.y, node.x))[0]


def dijkstra(mat, start, end=None):
    nodes = set()
    dist = dict()
    for node in list_of_units(mat, '.'):
        nodes.add(node)
        dist[node.ident] = INF
    nodes.add(start)
    dist[start.ident] = 0

    while nodes:
        node = find_closest(nodes, dist)
        if node is None:
            nodes.clear()
        else:
            nodes.remove(node)
            for node2 in node.neighbours:
                if node2.value == '.':
                    newdist = dist[node.ident] + 1
                    if newdist < dist[node2.ident]:
                        dist[node2.ident] = newdist

    if end is None:
        return dist
    else:
        return dist[end.ident]


def find_closest(nodes, dist):
    mini = INF
    xnode = None
    for node in nodes:
        if dist[node.ident] < mini:
            mini = dist[node.ident]
            xnode = node
    return xnode


def attack(unit, enemy, killed):
    enemy.hit_points -= unit.attack
    if enemy.hit_points <= 0:
        enemy.value = '.'
        enemy.hit_points = None
        killed.add(enemy)


def handle_round(mat):
    units = list_of_units(mat, 'EG')
    killed = set()

    for unit in units:
        # unit may have been killed (or killed and replaced by another unit)
        if unit in killed:  #unit.value == '.':
            continue

        enemies = list_of_units(mat, ENEMY[unit.value])
        if not enemies:
            return False

        in_contact = enemies_in_contact(unit)
        if in_contact:
            enemy = chose_enemy(in_contact)
            attack(unit, enemy, killed)
            continue

        in_range = get_in_range(enemies)
        if not in_range:
            continue

        closest_in_range_ = closest_in_range(mat, unit, in_range)
        if closest_in_range_.distance == INF:
            continue

        dist = dijkstra(mat, closest_in_range_)
        neighbours = list()
        for neighbour in unit.neighbours:
            if neighbour.value == '.':
                neighbours.append(neighbour)
                neighbour.distance = dist[neighbour.ident]
        if not neighbours:
            continue

        inter = sorted(neighbours, key=lambda node: (node.distance, node.y, node.x))[0]
        inter.value = unit.value
        inter.attack = unit.attack
        inter.hit_points = unit.hit_points
        unit.value = '.'
        unit.attack = None
        unit.hit_points = None
        in_contact = enemies_in_contact(inter)
        if in_contact:
            enemy = chose_enemy(in_contact)
            attack(inter, enemy, killed)

    return True


def run1(data):
    mat = load_nodes(data)

    count = 0
    print_mat(mat)
    while handle_round(mat):
        count += 1
        print(count)
        print_mat(mat)
        if count == 1000:
            return
    print('end')
    print_mat(mat)

    score = sum(unit.hit_points for unit in list_of_units(mat, 'EG')) * count
    return score


def run2(data):
    Node.attack = 3
    again = True
    while again:
        Node.attack += 1
        mat = load_nodes(data)
        print('--', Node.attack, '--' * 10)
        count = 0
        print_mat(mat)
        nelves = len(list_of_units(mat, 'E'))
        while handle_round(mat):
            count += 1
            print(count)
            print_mat(mat)
            nelves0 = nelves
            nelves = len(list_of_units(mat, 'E'))
            if nelves < nelves0:
                break
        again = len(list_of_units(mat, 'G')) != 0
        print('end')
        print_mat(mat)

    score = sum(unit.hit_points for unit in list_of_units(mat, 'EG')) * count
    return score


def code1():
    # assert run1(DATA1) == 27730
    # assert run1(DATA2) == 36334
    # assert run1(DATA3) == 39514
    # assert run1(DATA4) == 27755
    # assert run1(DATA5) == 28944
    # assert run1(DATA6) == 18740
    print('1>', run1(DATA0))


def code2():
    assert run2(DATA1) == 4988
    assert run2(DATA3) == 31284
    assert run2(DATA4) == 3478
    assert run2(DATA5) == 6474
    assert run2(DATA6) == 1140
    print('1>', run2(DATA0))


code2()
