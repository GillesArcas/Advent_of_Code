"""
--- 2016 --- Day 21: Scrambled Letters and Hash ---
"""


import re


EXAMPLES1 = (
    (('21-exemple1.txt', 'abcde'), 'decab'),
)

EXAMPLES2 = (
)

INPUT = ('21.txt', 'abcdefgh')


PATTERNS = (
    ('swappos', r'swap position (\d) with position (\d)'),
    ('swaplet', r'swap letter ([a-z]) with letter ([a-z])'),
    ('rotleft', r'rotate left (\d) step'),
    ('rotright', r'rotate right (\d) step'),
    ('rotbase', r'rotate based on position of letter ([a-z])'),
    ('revpos', r'reverse positions (\d) through (\d)'),
    ('movepos', r'move position (\d) to position (\d)')
)


def read_data(data):
    filename, root = data
    instructions = []
    with open(filename) as f:
        for line in f.readlines():
            for op, pat in PATTERNS:
                if match := re.match(pat, line):
                    instructions.append((op, *[int(_) if _.isdigit() else _ for _ in match.groups()]))
    return instructions, root


def apply(op, args, argstring):
    string = argstring[:]
    if op == 'swappos':
        string[args[0]], string[args[1]] = string[args[1]], string[args[0]]
    elif op == 'swaplet':
        pos1 = string.index(args[0])
        pos2 = string.index(args[1])
        string[pos1], string[pos2] = string[pos2], string[pos1]
    elif op == 'revpos':
        pos1 = args[0]
        pos2 = args[1]
        string[args[0]:args[1] + 1] = reversed(string[args[0]:args[1] + 1])
    elif op == 'rotleft':
        n = args[0]
        string = string[n:] + string[:n]
    elif op == 'rotright':
        n = args[0]
        string =  string[-n:] + string[:-n]
    elif op == 'movepos':
        pos1 = args[0]
        pos2 = args[1]
        if pos2 > pos1:
            c = string[pos1]
            string[pos1:pos1 + 1] = ''
            string[pos2:pos2] = c
        else:
            c = string[pos1]
            string[pos1:pos1 + 1] = ''
            string[pos2:pos2] = c
    elif op == 'rotbase':
        n = string.index(args[0])
        n = (n + 2 if (n >= 4) else n + 1) % len(string)
        string =  string[-n:] + string[:-n]
    else:
        pass
    return string


def unapply(op, args, string):
    if op == 'swappos':
        return apply('swappos', (args[1], args[0]), string)
    elif op == 'swaplet':
        return apply('swaplet', (args[1], args[0]), string)
    elif op == 'revpos':
        return apply('revpos', args, string)
    elif op == 'rotleft':
        return apply('rotright', args, string)
    elif op == 'rotright':
        return apply('rotleft', args, string)
    elif op == 'movepos':
        return apply('movepos', (args[1], args[0]), string)
    elif op == 'rotbase':
        for i in range(len(string)):
            s = apply('rotleft', (i,), string[:])
            if apply('rotbase', args, s) == string:
                return s
    else:
        pass
    return string


def check():
    # swappos x y s == swappos y x s
    s1 = list('abcdefgh')
    s2 = list('abcdefgh')
    for x in range(8):
        for y in range(8):
            assert apply('swappos', (x, y), s1) == apply('swappos', (y, x), s2)

    # swappos x y swappos y x s == s
    s1 = list('abcdefgh')
    s2 = list('abcdefgh')
    for x in range(8):
        for y in range(8):
            assert apply('swappos', (x, y), apply('swappos', (x, y), s1)) == s2

    # swaplet x y s == swaplet y x s
    s1 = list('abcdefgh')
    s2 = list('abcdefgh')
    for x in s1:
        for y in s1:
            assert apply('swaplet', (x, y), s1) == apply('swaplet', (y, x), s2)

    # swaplet x y swaplet y x s == s
    s1 = list('abcdefgh')
    s2 = list('abcdefgh')
    for x in s1:
        for y in s1:
            assert apply('swaplet', (x, y), apply('swaplet', (x, y), s1)) == s2

    # revpos x y revpos x y s == s
    s1 = list('abcdefgh')
    s2 = list('abcdefgh')
    for x in range(8):
        for y in range(8):
            assert apply('revpos', (x, y), apply('revpos', (x, y), s1)) == s2

    # revpos x x s == s
    s1 = list('abcdefgh')
    s2 = list('abcdefgh')
    for x in range(8):
        assert apply('revpos', (x, x), s1) == s2

    # revpos 0 len(s)-1 s == reversed(s)
    s1 = list('abcdefgh')
    s2 = list('abcdefgh')
    assert apply('revpos', (0, len(s1)-1), s1) == s2[::-1]

    # rotleft x s == rotright len(s)-x s
    s1 = list('abcdefgh')
    s2 = list('abcdefgh')
    for x in range(8):
        assert apply('rotleft', (x,), s1) == apply('rotright', (len(s2)-x,), s2)

    # rotleft x rotright x s == s
    s1 = list('abcdefgh')
    s2 = list('abcdefgh')
    for x in range(8):
        assert apply('rotleft', (x,), apply('rotright', (x,), s1)) == s2

    # len(s) * rotleft x s == s
    s1 = list('abcdefgh')
    s2 = list('abcdefgh')
    for _ in range(len(s1)):
        s1 = apply('rotleft', (1,), s1)
    assert s1 == s2

    # rotleft len(s) s == s
    s1 = list('abcdefgh')
    s2 = list('abcdefgh')
    assert apply('rotleft', (len(s1),), s1) == s2

    # movpos x y movpos y x s == s
    s1 = list('abcdefgh')
    s2 = list('abcdefgh')
    for x in range(8):
        for y in range(8):
            assert apply('movpos', (x, y), apply('movpos', (y, x), s1)) == s2


def code1(data):
    check()
    instructions, root = data
    string = list(root)
    for op, *args in instructions:
        string = apply(op, args, string)
    return ''.join(string)


def code2(data):
    instructions, _ = data
    string = list('fbgdceah')
    for op, *args in instructions[::-1]:
        string = unapply(op, args, string)

    assert code1((instructions, string)) == 'fbgdceah'

    return ''.join(string)


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
