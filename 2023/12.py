"""
--- Day 12: Hot Springs ---
"""


import re
import itertools


EXAMPLES1 = (
    ('12-exemple1.txt', 21),
)

EXAMPLES2 = (
    ('12-exemple1.txt', 525152),
)

INPUT = '12.txt'


def read_data(filename):
    data = []
    with open(filename) as f:
        for line in f:
            springs, s = line.strip().split()
            data.append((springs, [int(_) for _ in s.split(',')]))
    return data


def xset(target: list, indexes: list, value):
    result = target[:]
    for index in indexes:
        result[index] = value
    return result


def combinations(values):
    for leng in range(len(values) + 1):
        for comb in itertools.combinations(values, leng):
            yield comb


def arrangements(springs, groups):
    springs = list(springs)
    unknown = [i for i, char in enumerate(springs) if char == '?']
    missing = sum(groups) - sum(char == '#' for char in springs)
    # for comb in combinations(unknown):
    for comb in itertools.combinations(unknown, missing):
        arrangement = xset(springs, unknown, '.')
        yield ''.join(xset(arrangement, comb, '#'))


def spring_regex(groups):
    regex_groups = [f'#{{{_}}}' for _ in groups]
    return '^[.]*' + '[.]+'.join(regex_groups) + '[.]*$'


def spring_arrangements(springs, groups):
    """
    Handle one line of data
    """
    regex = spring_regex(groups)
    return sum(1 if re.search(regex, arrangement) else 0 for arrangement in arrangements(springs))


def spring_arrangements(springs, groups):
    """
    Handle one line of data
    """
    n = 0
    regex = spring_regex(groups)
    # print('---', springs, groups, regex)
    for arrangement in arrangements(springs, groups):
        # print(arrangement)
        if re.search(regex, arrangement):
            # print('match')
            n += 1
    print(springs, groups, n)
    return n


def spring_regex2(groups):
    regex_groups = [f'[#?]{{{_}}}' for _ in groups]
    return '^[^#]*' + '[^#]+'.join(regex_groups) + '[^#]*$'


def count(springs: str, regex):
    if re.search(regex, springs) is None:
        # print('fail ', regex, springs)
        return 0
    else:
        i = springs.find('?')
        if i < 0:
            # print('match', regex, springs)
            return 1
        else:
            return count(springs[:i] + '.' + springs[i + 1:], regex) +\
                   count(springs[:i] + '#' + springs[i + 1:], regex)


def spring_arrangements(springs, groups):
    """
    Handle one line of data
    """
    regex = spring_regex2(groups)
    # print('---', springs, groups, regex)
    n = count(springs, regex)
    # print(n)
    return n


def code1(data):
    return sum(spring_arrangements(springs, groups) for springs, groups in data)


def code2(data):
    count = 0
    for index, (springs, groups) in enumerate(data):
        springs2, groups2 = '?'.join([springs] * 5), groups + groups + groups + groups + groups
        r = spring_arrangements(springs2, groups2)
        print(index, springs, groups, r)
        count += r
    return count


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
