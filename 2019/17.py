import re
import intcode


DATA = '17.txt'


DELTA_I = (0, -1, 0, 1)
DELTA_J = (1, 0, -1, 0)


def code1():
    with open(DATA) as f:
        strcode = f.readline().strip()
        code = intcode.parse_data(strcode)
    computer = intcode.Intcode(code)
    computer.verbose_output = False

    computer.run([], return_output=False)
    s = ''.join([chr(_) for _ in computer.outvalues])
    zone = s.strip().splitlines()
    for _ in zone:
        print(_)

    r = 0
    for i, line in enumerate(zone[1:-1], 1):
        for j, char in enumerate(line[1:-1], 1):
            if char == line[j - 1] == line[j + 1] == zone[i - 1][j] == zone[i + 1][j] == '#':
                r += i * j

    print('1>', r)
    return computer, zone


def turn(zone, i, j, direction):
    """
    Detect if there is a turn at position i, j.
    Return:
        L or R and new direction if yes
        None if the scaffold continue
        'end' at the end of the scaffold
    """
    if direction == 0:
        if zone[i][j + 1] == '#':
            return False, None
        elif zone[i - 1][j] == '#':
            return 1, 'L'
        elif zone[i + 1][j] == '#':
            return 3, 'R'
        else:
            return 'end', None
    elif direction == 1:
        if zone[i - 1][j] == '#':
            return False, None
        elif zone[i][j - 1] == '#':
            return 2, 'L'
        elif zone[i][j + 1] == '#':
            return 0, 'R'
        else:
            return 'end', None
    elif direction == 2:
        if zone[i][j - 1] == '#':
            return False, None
        elif zone[i - 1][j] == '#':
            return 1, 'R'
        elif zone[i + 1][j] == '#':
            return 3, 'L'
        else:
            return 'end', None
    elif direction == 3:
        if zone[i + 1][j] == '#':
            return False, None
        elif zone[i][j - 1] == '#':
            return 2, 'R'
        elif zone[i][j + 1] == '#':
            return 0, 'L'
        else:
            return 'end', None
    else:
        assert False

def robot_position(zone):
    for i, line in enumerate(zone):
        for j, char in enumerate(line):
            if char in ('<', '>', 'v', '^'):
                return i, j


def cover(liste, pieces, nb):
    """
    Replace strings by pieces
    liste: list of strings to replace, or integers pointing to pieces
    pieces: pieces if initial strings
    nb: number of pieces to cover remaining strings in liste
    """
    first = next((x for x in liste if type(x) == str), None)
    if nb == 0 and not first:
        return liste, pieces
    elif (nb == 0 and first) or (nb and not first):
         return None, None
    else:
        count = len(re.findall(r'([LR],\d+,?)', first))
        for length in range(1, count + 1):
            m = re.match(r'(([LR],\d+,?){%d})' % length, first)
            A = m.group(1)

            if len(A) > 20:
                break

            newliste = list()
            newpieces = pieces[:]
            newpieces.append(A)
            segnum = len(newpieces)

            for x in liste:
                if type(x) == int:
                    newliste.append(x)
                else:
                    newliste.extend(re.split('(%s)' % A, x))

            newliste = [segnum if x == A else x for x in newliste if x]
            newliste, newpieces = cover(newliste, newpieces, nb - 1)
            if newliste:
                return newliste, newpieces
        return None, None


def code2(computer, zone):
    zone = ['!' * (len(zone[0]) + 2)] + [('!' + line + '!') for line in zone] + ['!' * (len(zone[0]) + 2)]
    i, j = robot_position(zone)

    # follow scaffold until the end
    direction = 2   # 0: E, 1: N, 2: W, 3: S
    path = ['L']
    while 1:
        nb_steps = 0
        while 1:
            new_dir, com = turn(zone, i, j, direction)
            if new_dir is False:
                i, j = i + DELTA_I[direction], j + DELTA_J[direction]
                nb_steps += 1
            else:
                break
        if new_dir == 'end':
            path.append(str(nb_steps))
            break
        else:
            path.append(str(nb_steps))
            path.append(com)
            direction = new_dir

    path = ','.join(path)
    print(path)
    routine, functions = cover([path + ','], [], 3)
    routine = ','.join('_ABC'[x] for x in routine)
    functions = [func[:-1] for func in functions]
    print(routine)
    for func in functions:
        print(func)
    msg = [ord(c) for c in routine] + [10]
    for func in functions:
        msg.extend([ord(c) for c in func] + [10])
    msg.extend([ord('n'), 10])
    print(msg)

    with open(DATA) as f:
        strcode = f.readline().strip()
        code = intcode.parse_data(strcode)
    computer = intcode.Intcode(code)
    computer.verbose_output = False
    computer.code[0] = 2
    computer.run(msg, return_output=False)
    #print(''.join(chr(x) for x in computer.outvalues))
    print('2>', computer.outvalues[-1])


computer, zone = code1()
code2(computer, zone)
