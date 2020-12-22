import re
from collections import defaultdict


EXEMPLE = 0
if EXEMPLE == 1:
    DATA = '14-exemple.txt'
elif EXEMPLE == 2:
    DATA = '14-exemple2.txt'
else:
    DATA = '14.txt'


def apply_mask1(mask, value):
    newbits = list()
    for i, (bitmask, bitvalue) in enumerate(zip(mask, f'{value:036b}')):
        if bitmask == 'X':
            newbits.append(bitvalue)
        else:
            newbits.append(bitmask)
    return int(''.join(newbits), 2)


def code1():
    memory = defaultdict(int)
    mask = 'X' * 36
    with open(DATA) as f:
        for line in (_.strip() for _ in f):
            if line.startswith('mask = '):
                mask = line.replace('mask = ', '')
                print(mask, sum(c == 'X' for c in mask))
            else:
                m = re.match(r'mem\[(\d+)\] = (\d+)', line)
                offset = int(m.group(1))
                value = int(m.group(2))
                memory[offset] = apply_mask1(mask, value)
    print('>', sum(memory.values()))


def apply_mask2(mask, offset):
    pattern_offset = list()
    for bitmask, bitoffset in zip(mask, f'{offset:036b}'):
        if bitmask == '0':
            pattern_offset.append(bitoffset)
        elif bitmask == '1':
            pattern_offset.append('1')
        else:
            pattern_offset.append('X')

    numx = sum(c == 'X' for c in mask)
    indexx = [i for i, c in enumerate(mask) if c == 'X']
    print('numx', numx, indexx)

    addresses = list()
    for n in range(2 ** numx):
        address = pattern_offset
        binary = f'{n:0{numx}b}'
        for index, bit in zip(indexx, binary):
            address[index] = bit
        addresses.append(''.join(address))

    return addresses


def code2():
    memory = defaultdict(int)
    mask = 'X' * 36
    with open(DATA) as f:
        for line in (_.strip() for _ in f):
            if line.startswith('mask = '):
                mask = line.replace('mask = ', '')
                print(mask, sum(c == 'X' for c in mask))
            else:
                m = re.match(r'mem\[(\d+)\] = (\d+)', line)
                offset = int(m.group(1))
                value = int(m.group(2))
                for address in apply_mask2(mask, offset):
                    memory[address] = value
    print('>', sum(memory.values()))


code1()
code2()
