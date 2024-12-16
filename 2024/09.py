"""
--- Day 9: Disk Fragmenter ---
"""


EXAMPLES1 = (
    ('09-exemple1.txt', 1928),
)

EXAMPLES2 = (
    ('09-exemple1.txt', 2858),
)

INPUT = '09.txt'


def read_data(filename):
    with open(filename) as f:
        return f.readline().strip()


def expanse(data):
    blocks = []
    for index, length in enumerate(data):
        if index % 2 == 0:
            for _ in range(int(length)):
                blocks.append(index // 2)
        else:
            for _ in range(int(length)):
                blocks.append('.')
    return blocks


def pack(blocks):
    free = 0
    while free < len(blocks):
        if blocks[free] != '.':
            free += 1
        else:
            last = blocks.pop()
            if last == '.':
                pass
            else:
                blocks[free] = last
                free += 1
    return blocks


def checksum(blocks):
    return sum(index * block for index, block in enumerate(blocks) if block != '.')


def code1(data):
    blocks = expanse(data)
    blocks = pack(blocks)
    return checksum(blocks)


def freespace(freeblocks, startfile, lenfile):
    for indexfree, (startfree, lenfree) in enumerate(freeblocks):
        if startfree >= startfile:
            return None
        if lenfree >= lenfile:
            return indexfree
    return None


def pack2(data, blocks):
    freeblocks = []
    fileblocks = []
    start = 0
    for index, length in enumerate(int(_) for _ in data):
        if index % 2 == 0:
            fileblocks.append([start, length])
        elif length == 0:
            pass
        else:
            freeblocks.append([start, length])
        start += length

    for startfile, lenfile in fileblocks[- 1:0:-1]:
        indexfree = freespace(freeblocks, startfile, lenfile)
        if indexfree is not None:
            startfree, lenfree = freeblocks[indexfree]
            for i in range(lenfile):
                blocks[startfree + i] = blocks[startfile + i]
                blocks[startfile + i] = '.'
            if lenfile == lenfree:
                del freeblocks[indexfree]
            else:
                freeblocks[indexfree] = [startfree + lenfile, lenfree - lenfile]

    return blocks


def code2(data):
    blocks = expanse(data)
    blocks = pack2(data, blocks)
    return checksum(blocks)


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
