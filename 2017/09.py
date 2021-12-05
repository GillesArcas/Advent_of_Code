
EXAMPLES1 = (
    ('{}', 1),
    ('{{{}}}', 6),
    ('{{},{}}', 5),
    ('{{{},{},{{}}}}', 16),
    ('{<a>,<a>,<a>,<a>}', 1),
    ('{{<ab>},{<ab>},{<ab>},{<ab>}}', 9),
    ('{{<!!>},{<!!>},{<!!>},{<!!>}}', 9),
    ('{{<a!>},{<a!>},{<a!>},{<ab>}}', 3)
)

EXAMPLES2 = (
    ('<>', 0),
    ('<random characters>', 17),
    ('<<<<>', 3),
    ('<{!>}>', 2),
    ('<!!>', 0),
    ('<!!!>>', 0 ),
    ('<{o"i!a,<{i<a>', 10)
 )

INPUT =  '09-input.txt'


def valchar(line):
    garbage = False
    cancel = False
    for c in line.strip():
        if cancel:
            cancel = False
        elif garbage:
            if c == '!':
                cancel = True
            elif c == '>':
                garbage = False
            else:
                pass
        elif c == '<':
            garbage = True
        else:
            yield c


def non_canceled_garbage(line):
    garbage = False
    cancel = False
    count = 0
    for c in line.strip():
        if cancel:
            cancel = False
        elif garbage:
            if c == '!':
                cancel = True
            elif c == '>':
                garbage = False
            else:
                count += 1
        elif c == '<':
            garbage = True
        else:
            pass
    return count


def read_data(fn, readfile=False):
    if readfile:
        with open(fn) as f:
            line = f.readline()
        return line
    else:
        return fn


def code1(data):
    data = ''.join(valchar(data))
    depth = 0
    sumdepth = 0
    for c in data:
        if c == '{':
            depth += 1
            sumdepth += depth
        elif c == '}':
            depth -= 1
        else:
            pass
    return sumdepth


def code2(data):
    return non_canceled_garbage(data)


def test(n, code, examples, myinput):
    for fn, result in examples:
        data = read_data(fn)
        assert code(data) == result, (data, result, code(data))

    print(f'{n}>', code(read_data(myinput, readfile=True)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
