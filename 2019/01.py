DATA = '01.txt'


def read_integers(data):
    with open(data) as f:
        for line in f:
            yield int(line)


def fuel1(mass):
    return mass // 3 - 2


def fuel2(mass):
    fuel = mass // 3 - 2
    result = fuel
    while (fuel := fuel // 3 - 2) > 0:
        result += fuel
    return result


def code1():
    print('>', sum(fuel1(mass) for mass in read_integers(DATA)))


def code2():
    print('>', sum(fuel2(mass) for mass in read_integers(DATA)))


code1()
code2()
