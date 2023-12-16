"""
--- Day 16: The Floor Will Be Lava ---
"""


EXAMPLES1 = (
    ('16-exemple1.txt', 46),
)

EXAMPLES2 = (
    ('16-exemple1.txt', 51),
)

INPUT = '16.txt'


def read_data(filename):
    with open(filename) as f:
        return [_.strip() for _ in f.readlines()]


def follow_beam(grid, i, j, dirn):
    beams = [[[] for j in range(len(grid[0]))] for i in range(len(grid))]
    stack = []
    stack.append((i, j, dirn))
    while stack:
        i, j, dirn = stack.pop(0)
        if not (0 <= i < len(grid) and 0 <= j < len(grid[0])):
            continue
        if dirn in beams[i][j]:
            continue
        beams[i][j].append(dirn)
        match dirn, grid[i][j]:
            case 'N', '.':
                stack.append((i - 1, j, 'N'))
            case 'E', '.':
                stack.append((i, j + 1, 'E'))
            case 'S', '.':
                stack.append((i + 1, j, 'S'))
            case 'W', '.':
                stack.append((i, j - 1, 'W'))

            case 'N', '/':
                stack.append((i, j + 1, 'E'))
            case 'E', '/':
                stack.append((i - 1, j, 'N'))
            case 'S', '/':
                stack.append((i, j - 1, 'W'))
            case 'W', '/':
                stack.append((i + 1, j, 'S'))

            case 'N', '\\':
                stack.append((i, j - 1, 'W'))
            case 'E', '\\':
                stack.append((i + 1, j, 'S'))
            case 'S', '\\':
                stack.append((i, j + 1, 'E'))
            case 'W', '\\':
                stack.append((i - 1, j, 'N'))

            case ('N', '-') | ('S', '-'):
                stack.append((i, j + 1, 'E'))
                stack.append((i, j - 1, 'W'))
            case 'E', '-':
                stack.append((i, j + 1, 'E'))
            case 'W', '-':
                stack.append((i, j - 1, 'W'))

            case ('E', '|') | ('W', '|'):
                stack.append((i - 1, j, 'N'))
                stack.append((i + 1, j, 'S'))
            case 'N', '|':
                stack.append((i - 1, j, 'N'))
            case 'S', '|':
                stack.append((i + 1, j, 'S'))

    count = 0
    for line in beams:
        count += sum(len(_) > 0 for _ in line)
    return count


def code1(grid):
    return follow_beam(grid, 0, 0, 'E')


def code2(grid):
    return max(
        max(follow_beam(grid, 0, j, 'S') for j in range(len(grid[0]))),
        max(follow_beam(grid, len(grid) - 1, j, 'N') for j in range(len(grid[0]))),
        max(follow_beam(grid, i, 0, 'E') for i in range(len(grid))),
        max(follow_beam(grid, i, len(grid[0]) - 1, 'W') for i in range(len(grid)))
    )


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
