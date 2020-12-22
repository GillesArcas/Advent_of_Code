import functools


DATASET = 1
if DATASET == 0:
    DATA = '12-exemple.txt'
else:
    DATA = '12.txt'


def code1():
    assert False  # éditin code2 sur code1
    with open(DATA) as f:
        i, j, d = 0, 0, 0
        # angles = set() {90, 180, 270}
        for line in f:
            instr = line[0]
            value = int(line.strip()[1:])
            if instr == 'N':
                i -= value
            elif instr == 'S':
                i += value
            elif instr == 'W':
                j -= value
            elif instr == 'E':
                j += value
            elif instr == 'L':
                pass
            elif instr == 'R':
                pass
            elif instr == 'F':
                if d == 0:
                    j += value
                elif d == 90:
                    i -= value
                elif d == 180:
                    j -= value
                elif d == 270:
                    i += value
                else:
                    assert False
            else:
                assert False
    print(abs(i) + abs(j))


def code2():
    # 23287 trop bas
    with open(DATA) as f:
        i, j, iw, jw = 0, 0, -1, 10
        for line in f:
            instr = line[0]
            value = int(line.strip()[1:])
            if instr == 'N':
                iw -= value
            elif instr == 'S':
                iw += value
            elif instr == 'W':
                jw -= value
            elif instr == 'E':
                jw += value
            elif instr == 'L':
                if value == 90:
                    jw, iw = iw, -jw
                elif value == 180:
                    jw, iw = -jw, -iw
                elif value == 270:
                    jw, iw = -iw, jw
            elif instr == 'R':
                if value == 90:
                    jw, iw = -iw, jw
                elif value == 180:
                    jw, iw = -jw, -iw
                elif value == 270:
                    jw, iw = iw, -jw
            elif instr == 'F':
                i += value * iw
                j += value * jw
            else:
                assert False
            print('%s %3d %4d %3d %3d %3d' % ( instr, value, i, j, iw, jw))
    print(abs(i) + abs(j))


#code1()
code2()
