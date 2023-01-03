"""
--- 2016 --- Day 18: Like a Rogue ---
"""


EXAMPLES1 = (
    ('18-exemple1.txt', 38),
)

EXAMPLES2 = (
)

INPUT = '18.txt'


def read_data(filename):
    with open(filename) as f:
        return f.read().strip()


def next_row(row):
    newrow = ['.'] * len(row)
    for index in range(1, len(row) - 1):
        pattern = row[index - 1:index + 2]
        if pattern in ('^^.', '.^^', '^..', '..^'):
            newrow[index] = '^'
    return ''.join(newrow)


def code1(row):
    nbrow = 10 if row == '.^^.^.^^^^' else 40
    row = '.' + row + '.'
    count = row[1:-1].count('.')
    for _ in range(nbrow - 1):
        row = next_row(row)
        count += row[1:-1].count('.')
    return count


def code2(row):
    nbrow = 400_000
    row = '.' + row + '.'
    count = row[1:-1].count('.')
    for _ in range(nbrow - 1):
        row = next_row(row)
        count += row[1:-1].count('.')
    return count


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
