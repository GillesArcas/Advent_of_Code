from collections import defaultdict, deque
import intcode


DATA = '15.txt'


DELTA_I = (None, -1, 1, 0, 0)
DELTA_J = (None, 0, 0, -1, 1)
UTURN = (None, 2, 1, 4, 3)
NOT_VISITED, WALL, FREE, OXYGEN = range(4)


def show_area(area, ix, jx):
    imin = float('inf')
    imax = -float('inf')
    jmin = float('inf')
    jmax = -float('inf')
    for i, row in area.items():
        imin = min(i, imin)
        imax = max(i, imax)
        for j, val in row.items():
            jmin = min(j, jmin)
            jmax = max(j, jmax)

    rows = [None] * (imax - imin + 1)
    for i, row in area.items():
        x = ['.'] * (jmax - jmin + 1)
        for j, val in row.items():
            if val == NOT_VISITED:
                pass
            elif val == WALL:
                x[j - jmin] = '#'
            elif val == FREE:
                x[j - jmin] = '-'
            elif val == OXYGEN:
                x[j - jmin] = 'O'

            if i == ix and j == jx:
                x[j - jmin] = 'X'
            elif i == 0 and j == 0:
                x[j - jmin] = '+'

        rows[i - imin] = ''.join(x)

    for row in rows:
        print(row)


def find_target(area):
    for i, row in area.items():
        for j, val in row.items():
            if val == OXYGEN:
                return i, j


def onestep(computer, area, direction, i, j):
    computer.run([direction], return_output=True)
    if computer.returned_on == 'terminate':
        pass

    status = computer.outvalues[-1]

    if status == 0:             # in front of wall
        area[i + DELTA_I[direction]][j + DELTA_J[direction]] = WALL
    else:
        i, j = i + DELTA_I[direction], j + DELTA_J[direction]
        if status == 1:         # moved
            area[i][j] = FREE
        elif status == 2:       # found
            area[i][j] = OXYGEN
        else:
            assert 0

    return i, j


def DFS(area, computer):
    i, j = 0, 0
    direction = 1
    area[i][j] = 2
    path = list()

    while 1:
        for test_direction in range(direction, 5):
            if area[i + DELTA_I[test_direction]][j + DELTA_J[test_direction]] == 0:
                i0, j0 = i, j
                i, j = onestep(computer, area, test_direction, i, j)
                if (i, j) != (i0, j0):
                    path.append(test_direction)
                    direction = 1
                    break
        else:
            if not path:
                break
            else:
                direction = path.pop()
                i, j = onestep(computer, area, UTURN[direction], i, j)
                direction += 1


# Below lists details all 4 possible movements from a cell
row = [-1, 0, 0, 1]
col = [0, -1, 1, 0]


def is_valid(area, visited, row, col):
    return area[row][col] != 1 and not visited[row][col]


def BFS(area, i, j, x, y):
    visited = defaultdict(lambda: defaultdict(bool))
    q = deque()
    visited[i][j] = True
    min_dist = float('inf')
    q.append((i, j, 0)) # (i, j, dist)

    while q:
        (i, j, dist) = q.popleft()
        if i == x and j == y:
            min_dist = dist
            break

        for k in range(4):
            if is_valid(area, visited, i + row[k], j + col[k]):
                visited[i + row[k]][j + col[k]] = True
                q.append((i + row[k], j + col[k], dist + 1))

    if min_dist != float('inf'):
        print('1>', min_dist)
    else:
        print('1> Not found')


def code1():
    with open(DATA) as f:
        strcode = f.readline().strip()
        code = intcode.parse_data(strcode)
    computer = intcode.Intcode(code)
    computer.verbose_output = False
    area = defaultdict(lambda: defaultdict(int))
    DFS(area, computer)
    show_area(area, 0, 0)
    i, j = find_target(area)
    BFS(area, 0, 0, i, j)
    return area, i, j


def code2(area, i, j):
    bord = set()
    bord.add((i, j))
    count = 0
    while bord:
        new_bord = set()
        for i, j in bord:
            for d in range(1, 5):
                i2, j2 = i + DELTA_I[d], j + DELTA_J[d]
                if area[i2][j2] == FREE:
                    area[i2][j2] = OXYGEN
                    new_bord.add((i2, j2))
        bord = new_bord
        if bord:
            count += 1
    print('2>', count)


area, i, j = code1()
code2(area, i, j)
