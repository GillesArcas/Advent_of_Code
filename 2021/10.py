
EXAMPLES1 = (
    ('10-exemple1.txt', 26397),
)

EXAMPLES2 = (
    ('10-exemple1.txt', 288957),
)

INPUT =  '10.txt'


CLOSEPAR = {'(': ')', '[': ']', '{': '}', '<': '>'}
COSTPAR = {')': 3, ']': 57, '}': 1197, '>': 25137}
COST2PAR = {')': 1, ']': 2, '}': 3, '>': 4}


def read_data(fn):
    data = list()
    with open(fn) as f:
        for line in f:
            line = line.strip()
            data.append(line)
    return data


def checkline1(line):
    stack = list()
    for c in line:
        if c in '([{<':
            stack.append(c)
        else:
            if c != CLOSEPAR[stack[-1]]:
                return c
            else:
                stack.pop()
    return None


def code1(data):
    score = 0
    for line in data:
        c = checkline1(line)
        if c is not None:
            score += COSTPAR[c]
    return score


def checkline2(line):
    stack = list()
    for c in line:
        if c in '([{<':
            stack.append(c)
        else:
            if c != CLOSEPAR[stack[-1]]:
                return None
            else:
                stack.pop()
    return ''.join([CLOSEPAR[c] for c in reversed(stack)])


def code2(data):
    scores = list()
    for line in data:
        s = checkline2(line)
        if s is not None:
            score = 0
            for c in s:
                score = score * 5 + COST2PAR[c]
            scores.append(score)
    return sorted(scores)[len(scores) // 2]


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
