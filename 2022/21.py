"""
--- 2022 --- Day 21: Monkey Math ---
"""


import re
import operator


EXAMPLES1 = (
    ('21-exemple1.txt', 152),
)

EXAMPLES2 = (
    ('21-exemple1.txt', 301),
)

INPUT = '21.txt'


OPS = (operator.add, operator.sub, operator.mul, operator.floordiv, operator.eq)


def read_data(filename):
    with open(filename) as f:
        data = f.readlines()

    jobs = {}
    for line in data:
        if match := re.match(r'([a-z]+): (\d+)', line):
            jobs[match.group(1)] = (identity, int(match.group(2)), 0)
        else:
            match = re.match(r'([a-z]+): ([a-z]+) ([-+*/]) ([a-z]+)', line)
            op = OPS['+-*/'.index(match.group(3))]
            jobs[match.group(1)] = (op, match.group(2), match.group(4))

    return jobs


def identity(x, _):
    return x


def evaluate(monkey, jobs):
    op, arg1, arg2 = jobs[monkey]
    return op(evaluate_arg(arg1, jobs), evaluate_arg(arg2, jobs))


def evaluate_arg(arg, jobs):
    if isinstance(arg, int):
        return arg
    else:
        return evaluate(arg, jobs)


def code1(jobs):
    return evaluate('root', jobs)


def depends(monkey, jobs):
    _, arg1, arg2 = jobs[monkey]
    if arg1 == 'humn' or arg2 == 'humn':
        return True
    else:
        return depends_arg(arg1, jobs) or depends_arg(arg2, jobs)


def depends_arg(arg, jobs):
    if isinstance(arg, int):
        return False
    else:
        return depends(arg, jobs)


def range_search(jobs, mini, maxi):
    _, arg1, arg2 = jobs['root']
    jobs['root'] = (operator.eq, arg1, arg2)
    for i in range(mini, maxi + 1):
        jobs['humn'] = (identity, i, 0)
        if evaluate('root', jobs):
            return i
    return None


def str_expr(monkey, jobs):
    op, arg1, arg2 = jobs[monkey]
    if op == identity:
        return arg1
    else:
        a1 = arg1 if arg1 == 'humn' else str_expr(arg1, jobs)
        a2 = arg2 if arg2 == 'humn' else str_expr(arg2, jobs)

        a1 = str(a1) if isinstance(a1, int) else f'({a1})'
        a2 = str(a2) if isinstance(a2, int) else f'({a2})'

        return f'{a1} {"+-*/=="[OPS.index(op)]} {a2}'


def arg_or_cte(monkey, jobs):
    if monkey == 'humn':
        return monkey
    elif jobs[monkey][0] == identity:
        return jobs[monkey][1]
    else:
        return monkey


def code2(jobs):
    dependant = set()
    for monkey, op in jobs.items():
        if depends(monkey, jobs):
            dependant.add(monkey)

    jobs2 = {}
    for monkey, op in jobs.items():
        if monkey in dependant:
            jobs2[monkey] = op
        else:
            jobs2[monkey] = (identity, evaluate(monkey, jobs), 0)

    op, arg1, arg2 = jobs2['root']
    jobs2['root'] = (operator.eq, arg1, arg2)
    print(str_expr('root', jobs2))

    arg = jobs2['root'][1]
    cte = [arg_or_cte(jobs2['root'][2], jobs2)] * 2

    while True:
        op, arg1, arg2 = jobs2[arg]
        a1 = arg_or_cte(arg1, jobs2)
        a2 = arg_or_cte(arg2, jobs2)
        print(a1, op, a2, '==', cte)

        if a1 == arg1 and a2 == arg2:
            break
        elif a1 == arg1:
            arg = arg1
            if op == operator.add:
                cte = (cte[0] - a2, cte[1] - a2)
            elif op == operator.sub:
                cte = (cte[0] + a2, cte[1] + a2)
            elif op == operator.mul:
                cte = (cte[0] // a2, cte[1] // a2)
            elif op == operator.floordiv:
                cte = (cte[0] * a2, cte[1] * a2 + a2 - 1)
        else:
            arg = arg2
            if op == operator.add:
                cte = (cte[0] - a1, cte[1] - a1)
            elif op == operator.sub:
                cte = (a1 - cte[0], a1 - cte[1])
            elif op == operator.mul:
                cte = (cte[0] // a1, cte[1] // a1)
            elif op == operator.floordiv:
                assert 0
        if arg1 == 'humn' or arg2 == 'humn':
            break

    return range_search(jobs, cte[0], cte[1])


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
