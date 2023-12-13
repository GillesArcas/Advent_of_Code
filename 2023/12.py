"""
--- Day 12: Hot Springs ---
"""


import re
import itertools
from functools import cache


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


# -- version 1 : génère à partir du spring pattern (avec itertools.combinations), matche avec regex construit sur les groupes


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


# -- version 2 : génère à partir du spring pattern (récursivement), matche avec regex construit sur les groupes


def spring_regex2(groups):
    regex_groups = [f'[#?]{{{_}}}' for _ in groups]
    return '^[^#]*' + '[^#]+'.join(regex_groups) + '[^#]*$'


def count(springs: str, regex):
    if re.search(regex, springs) is None:
        # print('fail', springs)
        return 0
    else:
        i = springs.find('?')
        if i < 0:
            # print('match', springs)
            return 1
        else:
            # print('cont', springs)
            return count(springs[:i] + '.' + springs[i + 1:], regex) +\
                   count(springs[:i] + '#' + springs[i + 1:], regex)


def spring_arrangements(springs, groups):
    """
    Handle one line of data
    """
    regex = spring_regex2(groups)
    print('---', springs, groups, regex)
    n = count(springs, regex)
    print(n)
    return n


# -- version 3 : génère à partir des groupes (par insertion de '.'), matche avec regex construit sur le pattern springs


def decomp(n, p):
    # décompose n en p entiers >= 0 to tq sum(decomp) == n
    if p == 1:
        yield [n]
    else:
        for i in range(n + 1):
            for dec in decomp(n - i, p - 1):
                yield [i] + dec


def groups_to_springs(springs, groups):
    """
    Handle one line of data
    """
    n1 = len(springs)
    n2 = sum(groups)
    # il faut ajouter n1 - n2 '.' avec au moins un '.' entre chaque groupe
    ninter = len(groups) - 1

    for dec in decomp(n1 - n2 - ninter, ninter + 2):
        # print(dec)
        cand = ['.' * dec[0]] +\
               ['#' * p + '.' * (q + 1) for p, q in zip(groups, dec[1:-1])] +\
               ['#' * groups[-1]] +\
               ['.' * dec[-1]]
        cand = ''.join(cand)
        yield cand


def spring_arrangements_3(springs, groups):
    """
    Handle one line of data
    """
    regex = '^' + springs.replace('.', '[.]').replace('?', '[.#]') + '$'
    print('---', springs, groups, regex)
    n = 0
    for cand in groups_to_springs(springs, groups):
        if re.match(regex, cand):
            print('match', cand)
            n += 1
    print(n)
    return n


# -- version 4


def match_group(springs, n):
    # print('>>', springs, n)
    for i, char in enumerate(springs):
        # print(springs, i, char)
        if char == '#':
            if match := re.match('([^.]{%d})([^#].*|)$' % n, springs[i:]):
                # print('match 1')
                if not match.group(2):
                    yield ''
                elif match.group(2)[0] == '.':
                    yield match.group(2)[0:]
                else:
                    yield '.' + match.group(2)[1:]
            # else:
            break
        elif char == '?':
            if match := re.match('([^.]{%d})([^#].*|)$' % n, springs[i:]):
                # print('match 2', match.group(2))
                if not match.group(2):
                    yield ''
                elif match.group(2)[0] == '.':
                    yield match.group(2)[0:]
                else:
                    yield '.' + match.group(2)[1:]
            else:
                pass
        elif char == '.':
            pass


# -- OK

def match_group(springs, n):
    # print('>>', springs, n)
    for i, char in enumerate(springs):
        # print(springs, i, char)
        if char == '.':
            pass
        elif match := re.match('([^.]{%d})([^#].*|)$' % n, springs[i:]):
            # print('match 1')
            if not match.group(2):
                yield ''
            elif match.group(2)[0] == '.':
                yield match.group(2)[0:]
            else:
                yield '.' + match.group(2)[1:]
        if char == '#':
            break


@cache
def match_group(springs, n):
    regex = re.compile('([^.]{%d})([^#].*|)$' % n)
    rests = []
    for i, char in enumerate(springs):
        if char == '.':
            pass
        elif match := regex.match(springs[i:]):
            if not match.group(2):
                rests.append('')
            elif match.group(2)[0] == '.':
                rests.append(match.group(2)[0:])
            else:
               rests.append('.' + match.group(2)[1:])
        if char == '#':
            break
    return rests


@cache
def match_group(springs, n):
    regex = re.compile('([^.]{%d})([^#].*|)$' % n)
    rests = []
    for i, char in enumerate(springs):
        if char == '.':
            continue
        elif match := regex.match(springs[i:]):
            if not match.group(2):
                rests.append('')
            elif match.group(2)[0] == '.':
                rests.append(match.group(2)[0:])
            else:
               rests.append('.' + match.group(2)[1:])
        if 1:  # char == '#':
            break
    return rests


def spring_arrangements(springs, groups):
    if not groups and re.match('[^#]*$', springs):
        return 1
    elif not groups:
        return 0
    else:
        count = 0
        for springs_rest in match_group(springs, groups[0]):
            count += spring_arrangements(springs_rest, groups[1:])
        return count


# -- Main


def code1(data):
    return sum(spring_arrangements(springs, groups) for springs, groups in data)


def unfold_groups(springs, groups, nfolds):
    return '?'.join([springs] * nfolds), groups * nfolds


def code2(data):
    count = 0
    for index, (springs, groups) in enumerate(data):
        springs2, groups2 = unfold_groups(springs, groups, 5)
        match_group.cache_clear()
        r = spring_arrangements(springs2, groups2)
        print(index, springs, groups, r)
        count += r
    return count


def code2_from(data, ifrom, n):
    count = 0
    for index, (springs, groups) in enumerate(data[ifrom:ifrom + n], ifrom):
        springs2, groups2 = unfold_groups(springs, groups, 5)
        match_group.cache_clear()
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
# test(2, code2, EXAMPLES2, INPUT)

# data = read_data(INPUT)
# ifrom = 400
# n = 200
# print('Partiel', ifrom, n, code2_from(data, ifrom, n))
