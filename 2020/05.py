with open('05.txt') as f:
    lines = [_.strip() for _ in f]

values = list()
for val in lines:
    val = val.replace('F', '0').replace('B', '1').replace('L', '0').replace('R', '1')
    values.append(int(val, 2))
values = sorted(values)


def code1():
    print(max(values))


def code2():
    for id1, id2 in zip(values[:-1], values[1:]):
        if id2 - id1 == 2:
            print(id1 + 1)
            break


code2()
