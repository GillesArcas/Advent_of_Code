import re


EXAMPLES1 = (
    ((5, '16-exemple1.txt'), 'baedc'),
)

EXAMPLES2 = (
)

INPUT = (16, '16.txt')


def read_data(data):
    size, codefn = data
    print(codefn)
    with open(codefn) as f:
        x = f.readline().strip().split(',')
    code = list()
    for c in x:
        match = re.match(r's(\d+)', c)
        if match:
            code.append(('s', int(match.group(1))))
            continue
        match = re.match(r'x(\d+)/(\d+)', c)
        if match:
            code.append(('x', int(match.group(1)), int(match.group(2))))
            continue
        match = re.match(r'p([a-z])/([a-z])', c)
        if match:
            code.append(('p', match.group(1), match.group(2)))
            continue
        assert 0
    return size, code


def apply_code(code, programs):
    # programs is a list
    programs = programs[:]  # TODO ?
    for op,*args in code:
        if op == 's':
            n, = args
            programs = programs[-n:] + programs[:-n]
            continue
        if op == 'x':
            i1, i2 = args
            programs[i1], programs[i2] = programs[i2], programs[i1]
            continue
        if op == 'p':
            v1, v2 = args
            i1 = programs.index(v1)
            i2 = programs.index(v2)
            programs[i1], programs[i2] = programs[i2], programs[i1]
            continue
        assert 0
    return programs


def repeat_code(code, programs, n):
    # programs is a list
    for _ in range(n):
        programs = apply_code(code, programs)
    return programs


def calc_period(code, programs):
    # programs is a list
    mem = set()
    mem.add(tuple(programs))
    for iteration in range(1_000_000_000):
        programs = apply_code(code, programs)
        if tuple(programs) in mem:
            return iteration + 1
    return None


def code1(data):
    size, code = data
    programs = list('abcdefghijklmnopqrstuvwxyz'[:size])
    programs = apply_code(code, programs)
    return ''.join(programs)


def code2(data):
    size, code = data
    programs0 = list('abcdefghijklmnopqrstuvwxyz'[:size])

    period = calc_period(code, programs0)

    programs = repeat_code(code, programs0, 1_000_000_000 % period)
    return ''.join(programs)


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
