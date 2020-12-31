import intcode


DATA = '09.txt'


def code1():
    with open(DATA) as f:
        strcode = f.readline().strip()
        code = intcode.parse_data(strcode)
    comp = intcode.Intcode(code)
    comp.run([1])
    print('1>', comp.outvalues)


def code2():
    with open(DATA) as f:
        strcode = f.readline().strip()
        code = intcode.parse_data(strcode)
    comp = intcode.Intcode(code)
    comp.run([2])
    print('2>', comp.outvalues)


code1()
code2()
