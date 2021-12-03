
EXAMPLES1 = (
    ('03-exemple1.txt', 198),
)

EXAMPLES2 = (
    ('03-exemple1.txt', 230),
)

INPUT =  '03.txt'


def read_list(fn):
    liste = list()
    with open(fn) as f:
        for line in f:
            liste.append([int(_) for _ in list(line.strip())])
    return liste


def gamma_rate(liste):
    bitsum = tuple(map(sum, zip(*liste)))
    newbits = ['0' if s <= len(liste) - s else '1' for s in bitsum]
    return int(''.join(newbits), 2)


def epsilon_rate(liste):
    bitsum = tuple(map(sum, zip(*liste)))
    newbits = ['0' if s > len(liste) - s else '1' for s in bitsum]
    return int(''.join(newbits), 2)


def code1(liste):
    gamma = gamma_rate(liste)
    epsilon = epsilon_rate(liste)
    return gamma * epsilon


def newbitmax(liste, nb_1):
    nb_0 = len(liste) - nb_1
    return '1' if nb_1 >= nb_0 else '0'


def newbitmin(liste, nb_1):
    nb_0 = len(liste) - nb_1
    return '0' if nb_1 >= nb_0 else '1'


def oxygen_rate(liste):
    for ibit in range(len(liste[0])):
        bitsum = tuple(map(sum, zip(*liste)))
        newbits = [newbitmax(liste, s) for s in bitsum]
        liste = [code for code in liste if str(code[ibit]) == newbits[ibit]]
        if len(liste) == 1:
            return int(''.join([str(_) for _ in liste[0]]), 2)


def co2_rate(liste):
    for ibit in range(len(liste[0])):
        bitsum = tuple(map(sum, zip(*liste)))
        newbits = [newbitmin(liste, s) for s in bitsum]
        liste = [code for code in liste if str(code[ibit]) == newbits[ibit]]
        if len(liste) == 1:
            return int(''.join([str(_) for _ in liste[0]]), 2)


def code2(liste):
    oxygen = oxygen_rate(liste)
    co2 = co2_rate(liste)
    return oxygen * co2


def test(n, code, examples, myinput):
    for fn, result in examples:
        data = read_list(fn)
        assert code(data) == result, (data, result, code(data))

    print(f'{n}>', code(read_list(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
