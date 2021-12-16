import math

EXAMPLES1 = (
    ('16-exemple1.txt', 31),
)

EXAMPLES2 = (
    ('16-exemple2.txt', 1),
)

INPUT =  '16.txt'


def read_data(fn):
    with open(fn) as f:
        line = f.readline().strip()
    s = bin(int(line, 16))[2:]
    while len(s) % 4:
        s = '0' + s
    return s


def applyop(typeid, args):
    if typeid == 0:
        return sum(args)
    elif typeid == 1:
        return math.prod(args)
    elif typeid == 2:
        return min(args)
    elif typeid == 3:
        return max(args)
    elif typeid == 5:
        assert len(args) == 2, args
        return 1 if args[0] > args[1] else 0
    elif typeid == 6:
        assert len(args) == 2, args
        return 1 if args[0] < args[1] else 0
    elif typeid == 7:
        assert len(args) == 2, args
        return 1 if args[0] == args[1] else 0
    else:
        assert 0


def decode(data, ptr=None):
    ptr = 0 if (ptr is None) else ptr
    ptr0 = ptr
    versum = 0
    version = int(data[ptr:ptr + 3], 2)
    ptr += 3
    versum += version
    typeid = int(data[ptr:ptr + 3], 2)
    ptr += 3
    if typeid == 4:
        # literal
        s = ''
        while 1:
            s += data[ptr + 1:ptr + 5]
            if data[ptr] == '0':
                ptr += 5
                break
            ptr += 5
        literal = int(s, 2)
        result = literal
    else:
        # operator
        args = list()
        if data[ptr] == '0':
            ptr += 1
            length = int(data[ptr:ptr + 15], 2)
            ptr += 15
            last = ptr + length
            while ptr < last:
                ptr, versum2, res = decode(data, ptr)
                versum += versum2
                args.append(res)
            result = applyop(typeid, args)
        else:
            ptr += 1
            number = int(data[ptr:ptr + 11], 2)
            ptr += 11
            for _ in range(number):
                ptr, versum2, res = decode(data, ptr)
                versum += versum2
                args.append(res)
            result = applyop(typeid, args)
    return ptr, versum, result


def code1(data):
    ptr, versum, result = decode(data)
    return versum


def code2(data):
    ptr, versum, result = decode(data)
    return result


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
