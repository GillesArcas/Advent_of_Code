import ast


def read_expr(string):
    for x in '0123456789':
        string = string.replace(x, '%s,' % x)
    for x in '+*':
        string = string.replace(x, '"%s",' % x)
    string = string.replace('(', '[')
    string = string.replace(')', '],')
    string = '[' + string + ']'
    expr = ast.literal_eval(string)
    return expr


def eval_expr(expr):
    if type(expr) == int:
        res = expr
    else:
        res = eval_expr(expr[0])
        p = 1
        while p < len(expr):
            op = expr[p]
            term = expr[p + 1]
            if op == '+':
                res += eval_expr(term)
            elif op == '*':
                res *= eval_expr(term)
            else:
                assert False
            p += 2

    return res


def aoc_eval(string_expr):
    res = eval_expr(read_expr(string_expr))
    return res


def code1():
    assert aoc_eval('1 + (2 * 3) + (4 * (5 + 6))') == 51
    assert aoc_eval('2 * 3 + (4 * 5)') == 26
    assert aoc_eval('5 + (8 * 3 + 9 + 3 * 4 * 3)') == 437
    assert aoc_eval('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))') == 12240
    assert aoc_eval('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2') == 13632
    print('OK')
    total = 0
    with open('18.txt') as f:
        for line in f:
            total += aoc_eval(line.strip())
    print('>', total)


def parenthese_plus(expr):
    if type(expr) == int:
        return expr
    else:
        newexpr = list()
        for term in expr:
            if term in ('+', '*'):
                newexpr.append(term)
            else:
                newexpr.append(parenthese_plus(term))
        expr = newexpr
        while '+' in expr:
            p = expr.index('+')
            expr1 = parenthese_plus(expr[p - 1])
            expr2 = parenthese_plus(expr[p + 1])
            expr[p - 1:p + 2] = [[expr1, '+', expr2]]
    return expr


def eval_expr2(expr):
    if type(expr) == int:
        return expr
    elif len(expr) == 1:
        return eval_expr2(expr[0])
    else:
        if expr[1] == '+':
            return eval_expr2(expr[0]) + eval_expr2(expr[2:])
        if expr[1] == '*':
            return eval_expr2(expr[0]) * eval_expr2(expr[2:])


def aoc_eval2(string_expr):
    x = parenthese_plus(read_expr(string_expr))
    #print(x)
    res = eval_expr2(x)
    return res


def code2():
    assert aoc_eval2('1 + 2 * 3 + 4 * 5 + 6') == 231
    assert aoc_eval2('1 + (2 * 3) + (4 * (5 + 6))') == 51
    assert aoc_eval2('2 * 3 + (4 * 5)') == 46
    assert aoc_eval2('5 + (8 * 3 + 9 + 3 * 4 * 3)') == 1445
    assert aoc_eval2('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))') == 669060
    assert aoc_eval2('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2') == 23340
    print('OK')
    total = 0
    with open('18.txt') as f:
        for line in f:
            total += aoc_eval2(line.strip())
    print('>', total)


code1()
code2()
