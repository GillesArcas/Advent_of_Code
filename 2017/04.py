
EXAMPLES1 = (
)

EXAMPLES2 = (
)

INPUT =  '04-input.txt'


def read_list(fn):
    """
    return the list of coordinate deltas (x, z)
    """
    liste = list()
    with open(fn) as f:
        return f.readlines()


def code1(liste):
    n = 0
    for line in liste:
        words = line.strip().split()
        if len(words) == len(set(words)):
            n += 1
    return n


def code2(liste):
    n = 0
    for line in liste:
        words = line.strip().split()
        words = tuple(''.join(sorted(word)) for word in words)
        if len(words) == len(set(words)):
            n += 1
    return n


def test(n, code, examples, myinput):
    for fn, result in examples:
        data = read_list(fn)
        assert code(data) == result, (data, result, code(data))

    print(f'{n}>', code(read_list(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
