import re
import copy
import colorama
from colorama import Fore, Style


EXAMPLES1 = (
    ('23-exemple1.txt', 12521),
)

EXAMPLES2 = (
    ('23-exemple1.txt', 44169),
)

INPUT = '23.txt'

INF = float('inf')


"""
Map representation:

place = (0, 0-10) hallway, 0 leftmost
        (1, 0-x)  room 1 , 0 topmost
        ...
"""
HALLWAYX = (0, 2, 4, 6, 8)



def read_map(lines):
    assert len(lines) in (5, 7)

    hallway = tuple(list(lines[1][1:11 + 1]))
    rooms = list()
    for j in [3, 5, 7, 9]:
        room = tuple(lines[i][j] for i in range(2, len(lines) - 1))
        rooms.append(room)

    return hallway, *rooms


def read_data(fn, n):
    with open(fn) as f:
        lines = f.readlines()

    if n == 2:
        extra = ['  #D#C#B#A#  ', '  #D#B#A#C#  ']
        lines = lines[:3] + extra + lines[3:]

    return read_map(lines)


def printed_map(podmap):
    hallway, *rooms = podmap
    view = list()
    view.append('#############')
    view.append('#' + ''.join(hallway) + '#')
    for x in zip(*rooms):
        view.append('###' + '#'.join(x) + '###')
    view.append('#############')
    return view


def print_map(podmap):
    for _ in printed_map(podmap):
        print(_)


def print_move(podmap1, podmap2, pod, pos):
    prtmap1 = printed_map(podmap1)
    prtmap2 = printed_map(podmap2)


    i = (0 if pod[0] == 0 else pod[1] + 1) + 1
    s = prtmap1[i]
    j = (pod[1] if pod[0] == 0 else HALLWAYX[pod[0]]) + 1
    prtmap1[i] = s[:j] + Fore.CYAN + s[j] + Style.RESET_ALL + s[j + 1:]

    i = (0 if pos[0] == 0 else pos[1] + 1) + 1
    s = prtmap2[i]
    j = (pos[1] if pos[0] == 0 else HALLWAYX[pos[0]]) + 1
    prtmap2[i] = s[:j] + Fore.CYAN + s[j] + Style.RESET_ALL + s[j + 1:]

    info = [''] * len(prtmap1)
    info[0] = f'pod: {pod}, dest: {pos}, linked: {linked(podmap1, pod, pos)}, energy: {energy(podmap1, pod, pos)}, dock: {pod_dock(podmap1, pod)}'
    for x, y, z in zip(prtmap1, prtmap2, info):
        print(x, '  ', y, '  ', z)
    print(podmap1)
    print()


def print_path(podmap, mapcache):
    while not finished(podmap):
        _, _, pod, best_move = mapcache[podmap]
        podmap2 = apply(podmap, pod, best_move)
        print_move(podmap, podmap2, pod, best_move)
        podmap = podmap2


def value(podmap, pod):
    return podmap[pod[0]][pod[1]]


def finished(podmap):
    return all(all(x == pod for x in r) for pod, r in zip('ABCD', podmap[1:]))


def empty(podmap):
    liste = list()
    for x, room in enumerate(podmap):
        liste.extend([(x, y) for y, value in enumerate(room) if value == '.'])
    return liste


def badpods(podmap):
    """
    bad pods which can move
    """
    hallway, *rooms = podmap
    pods = set()

    for x, v in enumerate(hallway):
        if v in 'ABCD':
            pods.add((0, x))

    for x, room in enumerate(rooms, 1):
        for y, v in enumerate(room):
            if y > 0 and any(_ != '.' for _ in room[:y]):
                continue
            if v in 'ABCD' and v != '.ABCD'[x]:
                pods.add((x, y))
            if v in 'ABCD' and v == '.ABCD'[x]:
                if any(w != v for w in room[y + 1:]):
                    pods.add((x, y))

    return pods


def pod_dock(podmap, pod):
    value = podmap[pod[0]][pod[1]]
    room_index = '.ABCD'.index(value)
    room = podmap[room_index]
    match = re.match(rf'^(\.*){value}*$', ''.join(room))
    if match is None:
        return None
    else:
        return (room_index, len(match.group(1)) - 1)


def dockable(podmap, pod):
    dock = pod_dock(podmap, pod)
    if dock := pod_dock(podmap, pod):
        if linked(podmap, pod, dock):
            return dock
        else:
            return None
    else:
        return None


def wrongroom(podmap, pod, empty):
    if empty[0] == 0:
        return False
    else:
        value = podmap[pod[0]][pod[1]]
        room_index = '.ABCD'.index(value)
        return room_index != empty[0]


def possible(podmap, pod):
    empties = empty(podmap)

    # avoid empty place in hallway in front of room
    empties = [x for x in empties if x[0] != 0 or x[1] not in [2, 4, 6, 8]]

    # avoid empty place if something in between
    empties = [x for x in empties if linked(podmap, pod, x)]

    # avoid empty place in room if not dock place
    dock = pod_dock(podmap, pod)
    if dock:
        empties = [x for x in empties if x[0] == 0 or x == dock]
    else:
        empties = [x for x in empties if x[0] == 0]

    # avoid wrong room
    empties = [x for x in empties if not wrongroom(podmap, pod, x)]

    return empties


def linked(podmap, place, empty):
    x1 = place[1] if (place[0] == 0) else HALLWAYX[place[0]]
    x2 = empty[1] if (empty[0] == 0) else HALLWAYX[empty[0]]
    mn = min(x1, x2)
    mx = max(x1, x2)
    if mn == place[1]:
        mn += 1
    if mx == place[1]:
        mx -= 1

    hallway = podmap[0]
    if any(hallway[j] != '.' for j in range(mn, mx + 1)):
        return False
    else:
        return True


def energy(podmap, place, empty):
    x1 = place[1] if (place[0] == 0) else HALLWAYX[place[0]]
    x2 = empty[1] if (empty[0] == 0) else HALLWAYX[empty[0]]
    mn = min(x1, x2)
    mx = max(x1, x2)
    y1 = 0 if place[0] == 0 else place[1] + 1
    y2 = 0 if empty[0] == 0 else empty[1] + 1
    return (mx - mn + y1 + y2) * 10 ** 'ABCD'.index(podmap[place[0]][place[1]])


def apply(podmap, pod, target):
    podmap = copy.deepcopy(podmap)
    podmap = [list(x) for x in podmap]
    podmap[target[0]][target[1]] = podmap[pod[0]][pod[1]]
    podmap[pod[0]][pod[1]] = '.'
    result = tuple(tuple(x) for x in podmap)
    return result


def strmap(podmap):
    return ''.join(podmap[0]) + ' ' + ' '.join([''.join(x) for x in podmap[1:]])


def next_move(podmap):
    """
    if one of the bad pods is dockable
        then return this pod and its dock
        else return the list of bad pods
    """
    bad = badpods(podmap)
    if not bad:
        return None, None
    else:
        for pod in bad:
            if move := dockable(podmap, pod):
                return pod, move
        return bad, None


def new_position(podmap, pod, target):
    newmap = apply(podmap, pod, target)
    score = energy(podmap, pod, target)
    return score, newmap


mapcache = dict()


def best_path(podmap, podpath):
    if podmap in mapcache:
        pass
    elif finished(podmap):
        mapcache[podmap] = 0, [], None, None
    else:
        pod, move = next_move(podmap)
        assert pod
        if move is not None:
            # dockable
            newmap = apply(podmap, pod, move)
            score_mov = energy(podmap, pod, move)
            score_path, *_ = best_path(newmap, podpath + [(pod, move)])
            score = score_mov + score_path
            mapcache[podmap] = score, None, pod, move
        else:
            best_pod = None
            best_move = None
            best_score = INF
            for pod in pod:
                moves = possible(podmap, pod)
                for move in moves:
                    assert linked(podmap, pod, move)
                    if (pod, move) in podpath:
                        continue
                    score_mov, newmap = new_position(podmap, pod, move)
                    score_path, *_ = best_path(newmap, podpath + [(pod, move)])
                    score = score_mov + score_path
                    if score < best_score:
                        best_pod = pod
                        best_move = move
                        best_score = score
            mapcache[podmap] = best_score, None, best_pod, best_move
    return mapcache[podmap]


def code1(podmap):
    score, *_ = best_path(podmap, [])
    return score


def code2(podmap):
    score, *_ = best_path(podmap, [])
    # print_path(podmap, mapcache)
    return score


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn, n)
        result = code(data)
        assert result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput, n)))


colorama.init()
test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
