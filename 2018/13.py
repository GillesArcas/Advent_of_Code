import re


DATA = '13.txt'


def get_data():
    with open(DATA) as f:
        amap = list(line.strip('\n') for line in f.readlines())
    carts = list()
    for y, line in enumerate(amap):
        for match in re.finditer('([<>^v])', line):
            c = match.group(1)
            x = match.start(1)
            d = '^>v<'.index(c)
            carts.append((y, x, d, 0))
    for y, _ in enumerate(amap):
        amap[y] = re.sub('([<>])', '-', amap[y])
        amap[y] = re.sub('([v^])', '|', amap[y])
    return amap, carts


def step(x, y, direction):
    deltax = [0, 1, 0, -1]
    deltay = [-1, 0, 1, 0]
    return x + deltax[direction], y + deltay[direction]


def next_step(amap, y, x, direction, nbinter):
    mapc = amap[y][x]
    if mapc == '+':
        if nbinter == 0:        # left
            direction = (direction + 3) % 4
        elif nbinter == 2:      # right
            direction = (direction + 1) % 4
        else:
            pass
        nbinter = (nbinter + 1) % 3
    elif mapc in '|-':
        pass
    elif mapc == '/':
        direction = [1, 0, 3, 2][direction]
    elif mapc == '\\':
        direction = [3, 2, 1, 0][direction]
    else:
        assert 0, (x, y, mapc)

    x, y = step(x, y, direction)
    return (y, x, direction, nbinter)


def collision(cart, carts):
    for cart2 in carts:
        if cart2 != cart:
            if cart2[:2] == cart[:2]:
                return True
    else:
        return False


def next_tick(amap, carts):
    carts.sort()
    for index, cart in enumerate(carts):
        cart2 = next_step(amap, *cart)
        carts[index] = cart2
        if collision(cart2, carts):
            print('1>', cart2[1], cart2[0])
            return False
    return True


def next_tick2(amap, carts):
    carts.sort()
    for index, cart in enumerate(carts):
        if cart is None:
            continue
        cart = next_step(amap, *cart)
        carts[index] = cart
        for index2, cart2 in enumerate(carts):
            if cart2 is None:
                continue
            if cart2 != cart:
                if cart2[:2] == cart[:2]:
                    carts[index] = None
                    carts[index2] = None

    cartcrashed = set(index for index, cart in enumerate(carts) if not cart)
    if cartcrashed:
        for index in sorted(cartcrashed, reverse=True):
            carts.pop(index)
        if len(carts) == 1:
            print('2>', carts[0][1], carts[0][0])
            return False
    return True


def print_map(amap, carts):
    bmap = [line[:] for line in amap]
    for y, x, direction, _ in carts:
        line = list(bmap[y])
        line[x] = '^>v<'[direction]
        bmap[y] = ''.join(line)
    for line in bmap:
        print(line)


def code1():
    amap, carts = get_data()
    while next_tick(amap, carts):
        pass
        # print_map(amap, carts)


def code2():
    amap, carts = get_data()
    # print_map(amap, carts)
    while next_tick2(amap, carts):
        pass
        # print_map(amap, carts)


code1()
code2()
