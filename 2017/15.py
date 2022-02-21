
EXAMPLES1 = (
    ((65, 8921), 588),
)

EXAMPLES2 = (
    ((65, 8921), 309),
)

INPUT = (679, 771)


def read_data(data):
    return data


def code1(data):
    a, b = data
    count = 0
    iterations = 40_000_000
    for _ in range(iterations):
        a = a * 16807 % 2147483647
        b = b * 48271 % 2147483647
        hex_a = hex(a)[-4:]
        hex_b = hex(b)[-4:]
        if hex_a == hex_b:
            count += 1
    return count


def next_a(a):
    a = a * 16807 % 2147483647
    while a % 4 != 0:
        a = a * 16807 % 2147483647
    return a


def next_b(b):
    b = b * 48271 % 2147483647
    while b % 8 != 0:
        b = b * 48271 % 2147483647
    return b


def code2(data):
    a, b = data
    count = 0
    iterations = 5_000_000
    for _ in range(iterations):
        a = next_a(a)
        b = next_b(b)
        hex_a = hex(a)[-4:]
        hex_b = hex(b)[-4:]
        if hex_a == hex_b:
            count += 1
    return count


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
