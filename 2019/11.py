from collections import defaultdict
import intcode


DATA = '11.txt'


def run_robot(panels, computer):
    pos = 0, 0      # i, j
    direction = 0   # 0 N, 1 E, 2 S, 3 W

    while True:
        computer.run([panels[pos]], return_output=True)
        if computer.returned_on == 'terminate':
            break

        color = computer.outvalues[-1]
        computer.run([], return_output=True)
        turn = computer.outvalues[-1]

        panels[pos] = color

        if turn == 0:           # left
            direction = (direction + 3) % 4
        else:                   # right
            direction = (direction + 1) % 4

        i, j = pos
        if direction == 0:      # N
            pos = i - 1, j
        elif direction == 1:    # E
            pos = i, j + 1
        elif direction == 2:    # S
            pos = i + 1, j
        elif direction == 3:    # W
            pos = i, j - 1
        else:
            assert False

    return panels


def code1():
    with open(DATA) as f:
        strcode = f.readline().strip()
        code = intcode.parse_data(strcode)
    computer = intcode.Intcode(code)
    computer.verbose_output = False

    panels = defaultdict(int)
    panels = run_robot(panels, computer)
    print('1>', len(panels))


def code2():
    with open(DATA) as f:
        strcode = f.readline().strip()
        code = intcode.parse_data(strcode)
    computer = intcode.Intcode(code)
    computer.verbose_output = False

    panels = defaultdict(int)
    panels[(0, 0)] = 1
    panels = run_robot(panels, computer)
    print('2>', len(panels))

    imin, imax = float('inf'), -float('inf')
    jmin, jmax = float('inf'), -float('inf')
    for i, j in panels.keys():
        imin = min(imin, i)
        imax = max(imax, i)
        jmin = min(jmin, j)
        jmax = max(jmax, j)
    print(imin, imax, jmin, jmax)
    for i in range(imin, imax + 1):
        s = [panels[(i, j)] for j in range(jmin, jmax + 1)]
        print(''.join(['.' if _ == 0 else '#' for _ in s]))


code1()
code2()
