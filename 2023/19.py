"""
--- Day 19: Aplenty ---
"""


import re
import math


EXAMPLES1 = (
    ('19-exemple1.txt', 19114),
)

EXAMPLES2 = (
    ('19-exemple1.txt', 167409079868000),
)

INPUT = '19.txt'


def read_data(filename):
    with open(filename) as f:
        text = f.read()

    workflows = {}
    for wf in re.findall(r'^([a-z]+)\{(.+)\}$', text, flags=re.M):
        name = wf[0]
        workflows[name] = []
        for s in wf[1].split(','):
            if re.match(r'[ARa-z]+$', s):
                workflows[name].append(s)
            else:
                match = re.match(r'([xmas])([<>])(\d+):([ARa-z]+)', s)
                workflows[name].append((match[1], match[2], int(match[3]), match[4]))

    parts = [eval(f'dict({_})') for _ in re.findall('^{(.+)}$', text, flags=re.M)]

    return workflows, parts


def apply_op(op, v1, v2):
    if op == '<':
        return v1 < v2
    else:
        return v1 > v2


def apply_workflow(workflow, parts):
    for rule in workflow:
        if rule == 'A':
            return True
        elif rule == 'R':
            return False
        elif isinstance(rule, str):
            return rule
        else:
            var, op, val, name = rule
            if apply_op(op, parts[var], val):
                return True if name == 'A' else False if name == 'R' else name


def apply_workflows(workflows, parts):
    name = 'in'
    while 1:
        r = apply_workflow(workflows[name], parts)
        if r in (True, False):
            return r
        else:
            name = r


def code1(data):
    workflows, parts = data
    count = 0
    for p in parts:
        if apply_workflows(workflows, p):
            count += sum(p.values())
    return count


def paths_to_accept(workflows, paths, path, rule):
    """
    rule: ((x, op, v, A|R|rulename)|A|R|rulename)+ full or partial
    """
    neg = {'<': '>=', '>': '<='}
    r = rule[0]
    if r == 'A':
        paths.append(path)
    elif r == 'R':
        pass
    elif isinstance(r, str):
        paths_to_accept(workflows, paths, path, workflows[r])
    else:
        x, op, v, r = r
        paths_to_accept(workflows, paths, path + [(x, op, v)], [r])
        paths_to_accept(workflows, paths, path + [(x, neg[op], v)], rule[1:])


def path_contribution(path):
    bounds = {_:[1, 4000] for _ in 'xmas'}
    for x, op, v in path:
        if op == '<':
            bounds[x][1] = min(bounds[x][1], v - 1)
        elif op =='<=':
            bounds[x][1] = min(bounds[x][1], v)
        elif op =='>':
            bounds[x][0] = max(bounds[x][0], v + 1)
        elif op == '>=':
            bounds[x][0] = max(bounds[x][0], v)
    return math.prod(_[1] - _[0] + 1 for _ in bounds.values())


def code2(data):
    workflows, _ = data
    paths = []
    paths_to_accept(workflows, paths, [], workflows['in'])
    count = 0
    for path in paths:
        n = path_contribution(path)
        count += n
    return count


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
