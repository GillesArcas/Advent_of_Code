from collections import defaultdict


def spoken(liste):
    if liste[0] not in liste[1:]:
        return [0] + liste
    else:
        index = liste[1:].index(liste[0]) + 1
        # print(liste, index)
        return [index] + liste


def spoken_nth(string, nth):
    liste = list(reversed([int(_) for _ in string.split(',')]))
    while True:
        liste = spoken(liste)
        if len(liste) == nth:
            return liste[0]


def code1():
    assert spoken_nth('0,3,6', 10) == 0
    assert spoken_nth('1,3,2', 2020) == 1
    assert spoken_nth('2,1,3', 2020) == 10
    assert spoken_nth('1,2,3', 2020) == 27
    assert spoken_nth('2,3,1', 2020) == 78
    assert spoken_nth('3,2,1', 2020) == 438
    assert spoken_nth('3,1,2', 2020) == 1836
    print('>', spoken_nth('2,0,1,9,5,19', 2020))


def spoken(liste):
    if liste[0] not in liste[1:]:
        return [0] + liste
    else:
        index = liste[1:].index(liste[0]) + 1
        # print(liste, index)
        return [index] + liste


def spoken_nth(string, nth):
    seen = dict()
    vals = [int(_) for _ in string.split(',')]
    last = -1
    for index, val in enumerate(vals):
        seen[last] = index
        last = val

    for p in range(len(vals) + 1, nth + 1):
        last0 = last
        seen0 = {k:v for k,v in seen.items()}
        if last not in seen:
            seen[last] = p
            last = 0
        else:
            seen[last] = p
            last = p - 1 - seen0[last]
        print(p, last0, seen0, last)


def spoken_nth(string, nth):
    seen = dict()
    vals = [int(_) for _ in string.split(',')]
    spoken = -1
    for index, val in enumerate(vals):
        seen[spoken] = index
        spoken = val

    for p in range(len(vals) + 1, nth + 1):
        if spoken not in seen:
            newspoken = 0
        else:
            newspoken = p - 1 - seen[spoken]
        seen[spoken] = p - 1
        print(p, newspoken, spoken, seen)


def spoken_nth(string, nth):
    seen = defaultdict(list)
    vals = [int(_) for _ in string.split(',')]
    for index, val in enumerate(vals, 1):
        spoken = val
        seen[spoken].append(index)

    for p in range(len(vals) + 1, nth + 1):
        spoken0 = spoken
        if len(seen[spoken0]) == 1:
            spoken = 0
        else:
            spoken = seen[spoken0][-1] - seen[spoken0][-2]
        seen[spoken].append(p)
        seen[spoken] = seen[spoken][-2:]
        #print(p, spoken0, spoken, seen)
    return spoken


def code2():
    assert spoken_nth('0,3,6', 10) == 0
    assert spoken_nth('0,3,6', 2020) == 436
    assert spoken_nth('1,3,2', 2020) == 1
    assert spoken_nth('2,1,3', 2020) == 10
    assert spoken_nth('1,2,3', 2020) == 27
    assert spoken_nth('2,3,1', 2020) == 78
    assert spoken_nth('3,2,1', 2020) == 438
    assert spoken_nth('3,1,2', 2020) == 1836
    assert spoken_nth('0,3,6', 30000000) == 175594
    print('>', spoken_nth('2,0,1,9,5,19', 30000000))



#code1()
code2()
