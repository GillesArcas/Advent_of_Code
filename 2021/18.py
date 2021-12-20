import copy
import itertools


EXAMPLES1 = (
    ('18-exemple2.txt', 4140),
)

EXAMPLES2 = (
    ('18-exemple2.txt', 3993),
)

INPUT =  '18.txt'


def read_data(fn):
    with open(fn) as f:
        return [eval(line) for line in f.readlines()]


# explode


class TransformDone(Exception):
    pass


def linkbackrec(sfint, prev, back):
    if isinstance(sfint, int):
        pass
    else:
        back[id(sfint)] = prev
        linkbackrec(sfint[0], sfint, back)
        linkbackrec(sfint[1], sfint, back)


def linkback(sfint):
    back = dict()
    linkbackrec(sfint, None, back)
    return back


def addleft(sfint, back):
    val = sfint[0]
    prev = back[id(sfint)]
    while prev and id(sfint) == id(prev[0]):
        sfint = prev
        prev = back[id(sfint)]
    if prev:
        if isinstance(prev[0], int):
            prev[0] += val
        else:
            prev = prev[0]
            while not isinstance(prev[1], int):
                prev = prev[1]
            prev[1] += val


def addright(sfint, back):
    val = sfint[1]
    prev = back[id(sfint)]
    while prev and id(sfint) == id(prev[1]):
        sfint = prev
        prev = back[id(sfint)]
    if prev:
        if isinstance(prev[1], int):
            prev[1] += val
        else:
            prev = prev[1]
            while not isinstance(prev[0], int):
                prev = prev[0]
            prev[0] += val


def explode(sfint):
    back = linkback(sfint)
    try:
        exploderec(sfint, back)
    except TransformDone:
        pass
    return sfint


def exploderec(sfint, back, depth=0):
    if isinstance(sfint, int):
        pass
    elif depth < 4:
        exploderec(sfint[0], back, depth + 1)
        exploderec(sfint[1], back, depth + 1)
    else:
        # pair (m, n) of depth 5
        addleft(sfint, back)
        addright(sfint, back)
        prev = back[id(sfint)]
        if prev[0] == sfint:
            prev[0] = 0
        else:
            prev[1] = 0
        raise TransformDone


def compare(x, y):
    if x == y:
        pass
    else:
        print(x, y)
        assert 0


# compare(explode([[[[[9,8],1],2],3],4]), [[[[0,9],2],3],4])
# compare(explode([7,[6,[5,[4,[3,2]]]]]), [7,[6,[5,[7,0]]]])
# compare(explode([[6,[5,[4,[3,2]]]],1]), [[6,[5,[7,0]]],3])
# compare(explode([[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]), [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]])
# compare(explode([[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]), [[3,[2,[8,0]]],[9,[5,[7,0]]]])
# compare(explode([[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]],[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]]), [[[[0,[13,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]],[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]])


# split


def split(sfint):
    try:
        splitrec(sfint)
    except TransformDone:
        pass
    return sfint


def splitrec(sfint):
    if isinstance(sfint, int):
        return

    if isinstance(sfint[0], int):
        if sfint[0] >= 10:
            sfint[0] = [sfint[0] // 2, sfint[0] - sfint[0] // 2]
            raise TransformDone
    else:
        splitrec(sfint[0])

    if isinstance(sfint[1], int):
        if sfint[1] >= 10:
            sfint[1] = [sfint[1] // 2, sfint[1] - sfint[1] // 2]
            raise TransformDone
    else:
        splitrec(sfint[1])


# compare(split([[[[0,7],4],[15,[0,13]]],[1,1]]), [[[[0,7],4],[[7,8],[0,13]]],[1,1]])
# compare(split([[[[0,7],4],[[7,8],[0,13]]],[1,1]]), [[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]])


# reduce


def reduce(sfint):
    while 1:
        sfint0 = copy.deepcopy(sfint)
        sfint = explode(sfint)
        if sfint != sfint0:
            continue
        sfint = split(sfint)
        if sfint == sfint0:
            return sfint


# compare(reduce([[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]), [[[[0,7],4],[[7,8],[6,0]]],[8,1]])

# https://old.reddit.com/r/adventofcode/comments/rjgfyr/2021_day_18_hint_all_explodes_and_splits_in_the/
# compare(reduce([[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]],[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]]), [[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]])
# compare(reduce([[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]],[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]]), [[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]])
# compare(reduce([[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]],[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]]), [[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]])
compare(reduce([[[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]],[7,[5,[[3,8],[1,4]]]]]), [[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]])


# addition


def sfadd(sfint1, sfint2, *sfints):
    sfint1 = copy.deepcopy(sfint1)
    sfint2 = copy.deepcopy(sfint2)
    result = reduce([sfint1, sfint2])
    for sfint in sfints:
        result = reduce([result, sfint])
    return result


# compare(sfadd([1, 1], [2, 2], [3, 3], [4, 4]), [[[[1,1],[2,2]],[3,3]],[4,4]])
# compare(sfadd([1, 1], [2, 2], [3, 3], [4, 4], [5, 5]), [[[[3,0],[5,3]],[4,4]],[5,5]])
# compare(sfadd([1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6]), [[[[5,0],[7,4]],[5,5]],[6,6]])
# compare(sfadd([[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]], [[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]),
        # [[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]])

compare(sfadd(*read_data('18-exemple1.txt')), [[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]])
compare(sfadd(*read_data('18-exemple2.txt')), [[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]])


# magnitude


def magnitude(sfint):
    if isinstance(sfint, int):
        return sfint
    else:
        return 3 * magnitude(sfint[0]) + 2 * magnitude(sfint[1])


# main


def code1(data):
    return magnitude(sfadd(*data))


def code2(data):
    maxmag = 0
    for x, y in itertools.permutations(data, 2):
        sfsum = sfadd(x, y)
        mag = magnitude(sfsum)
        if mag > maxmag:
            maxmag = mag
    return maxmag


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
