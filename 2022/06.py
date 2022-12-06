"""
--- 2022 --- Day 6: Tuning Trouble ---
"""


EXAMPLES1 = (
    ('mjqjpqmgbljsphdztnvjfqwrcgsmlb', 7),
    ('bvwbjplbgvbhsrlpgdmjqwftvncz', 5),
)

EXAMPLES2 = (
    ('mjqjpqmgbljsphdztnvjfqwrcgsmlb', 19),
    ('bvwbjplbgvbhsrlpgdmjqwftvncz', 23),
)

INPUT = '06.txt'


def read_data(data):
    if data.endswith('.txt'):
        with open(data) as f:
            return f.read().strip()
    else:
        return data


def code1(data):
    for i in range(len(data) - 4):
        if len(set(data[i:i + 4])) == 4:
            return i + 3 + 1    # +1 because 1-based
    return None


def code2(data):
    for i in range(0, len(data) - 14):
        if len(set(data[i:i + 14])) == 14:
            return i + 13 + 1
    return None


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
