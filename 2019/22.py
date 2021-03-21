import math


# https://fr.wikipedia.org/wiki/Congruence_lin%C3%A9aire
# https://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python


REV, CUT, INC = 0, 1, 2


def get_data(n):
    if n == 0:
        with open('22.txt') as f:
            shuffle = f.read()
        length = 10007
        result = None
    elif n == 20:
        with open('22.txt') as f:
            shuffle = f.read()
        length = 119315717514047
        result = None
    elif n == 1:
        shuffle = '''
            deal with increment 7
            deal into new stack
            deal into new stack
        '''
        length = 10
        result = [int(_) for _ in '0 3 6 9 2 5 8 1 4 7'.split()]
    elif n == 2:
        shuffle = '''
            cut 6
            deal with increment 7
            deal into new stack
        '''
        length = 10
        result = [int(_) for _ in '3 0 7 4 1 8 5 2 9 6'.split()]
    elif n == 3:
        shuffle = '''
            deal with increment 7
            deal with increment 9
            cut -2
        '''
        length = 10
        result = [int(_) for _ in '6 3 0 7 4 1 8 5 2 9'.split()]
    elif n == 4:
        shuffle = '''
            deal into new stack
            cut -2
            deal with increment 7
            cut 8
            cut -4
            deal with increment 7
            cut 3
            deal with increment 9
            deal with increment 3
            cut -1
        '''
        length = 10
        result = [int(_) for _ in '9 2 5 8 1 4 7 0 3 6'.split()]

    shuffle_code = list()
    for shuf in [_.strip() for _ in shuffle.splitlines()]:
        if shuf == 'deal into new stack':
            shuffle_code.append((REV, None))
        elif shuf.startswith('cut '):
            stack =  shuffle_code.append((CUT, int(shuf[len('cut '):])))
        elif shuf.startswith('deal with increment '):
            stack =  shuffle_code.append((INC, int(shuf[len('deal with increment '):])))

    return shuffle_code, length, result


def deal_into_new_stack(stack):
    return list(reversed(stack))


def cut(stack, n):
    return stack[n:] + stack[:n]


def deal_with_increment(stack, n):
    stack2 = stack[:]
    new = [-1] * len(stack)
    p = 0
    new[p] = stack2.pop(0)
    while stack2:
        p = (p + n) % len(stack)
        new[p] = stack2.pop(0)
    return new


def apply(shuffle, stack):
    for op, arg in shuffle:
        if op == REV:
            stack = deal_into_new_stack(stack)
        elif op == CUT:
            stack = cut(stack, arg)
        elif op == INC:
            stack = deal_with_increment(stack, arg)
    return stack


def solve_modular_equation(a, b, c):
    """
    Find solution of ax % b = c (a and b relative primes, ie assume gcd(a, b) == 1)
    pow(a, -1, mod=b) computes the modular multiplicative inverse for python >= 3.8
    """
    return (pow(a, -1, mod=b) * c) % b


def direct_index_new_stack(L, index):
    # return L - index - 1
    return (-index - 1) % L


def reverse_index_new_stack(L, index):
    return direct_index_new_stack(L, index)


def coef_direct_new_stack():
    return -1, -1


def coef_reverse_new_stack():
    return -1, -1


def direct_index_cut(L, n, index):
    return (index - n) % L


def reverse_index_cut(L, n, index):
    return direct_index_cut(L, L - n, index)


def coef_direct_cut(n):
    return 1, -n


def coef_reverse_cut(n, L):
    return 1, n


def direct_index_increment(L, p, index):
    return (index * p) % L


def reverse_index_increment(L, p, index):
    return (pow(p, -1, mod=L) * index) % L


def coef_direct_increment(p):
    return p, 0


def coef_reverse_increment(p, L):
    return pow(p, -1, mod=L), 0


def forward_index_v1(shuffle, L, index, repeat=1):
    """
    Find destination index handling transformation one by one
    """
    for _ in range(repeat):
        for op, arg in shuffle:
            if op == REV:
                index = direct_index_new_stack(L, index)
            elif op == CUT:
                index = direct_index_cut(L, arg, index)
            elif op == INC:
                index = direct_index_increment(L, arg, index)
    return index


def backward_index_v1(shuffle, L, index, repeat=1):
    """
    Find origin index handling transformation one by one
    """
    for _ in range(repeat):
        for op, arg in reversed(shuffle):
            if op == REV:
                index = reverse_index_new_stack(L, index)
            elif op == CUT:
                index = reverse_index_cut(L, arg, index)
            elif op == INC:
                index = reverse_index_increment(L, arg, index)
    return index


def direct_coefficients(shuffle, L, index, repeat=1):
    """
    Compute coefficients of complete direct transformation
    """
    a, b = 1, 0
    for op, arg in shuffle:
        if op == REV:
            a2, b2 = coef_direct_new_stack()
        elif op == CUT:
            direct_index_cut(L, arg, index)
            a2, b2 = coef_direct_cut(arg)
        elif op == INC:
            a2, b2 = coef_direct_increment(arg)
        a = (a2 * a) % L
        b = (a2 * b + b2) % L

    if repeat == 1:
        return a, b
    else:
        a_repeat = pow(a, repeat, mod=L)
        b_repeat = ((a_repeat - 1) * pow(a - 1, -1, mod=L) * b) % L
        return a_repeat, b_repeat


def reverse_coefficients(shuffle, L, index, repeat=1):
    """
    Compute coefficients of complete direct transformation
    """
    a, b = 1, 0
    for op, arg in reversed(shuffle):
        if op == REV:
            a2, b2 = coef_reverse_new_stack()
        elif op == CUT:
            a2, b2 = coef_reverse_cut(arg, L)
        elif op == INC:
            a2, b2 = coef_reverse_increment(arg, L)
        a = (a2 * a) % L
        b = (a2 * b + b2) % L

    if repeat == 1:
        return a, b
    else:
        a_repeat = pow(a, repeat, mod=L)
        b_repeat = ((a_repeat - 1) * pow(a - 1, -1, mod=L) * b) % L
        return a_repeat, b_repeat


def forward_index(shuffle, L, index, repeat=1):
    """
    Find destination index using coefficients of complete shuffle
    """
    a, b = direct_coefficients(shuffle, L, index, repeat)
    return (a * index + b) % L


def backward_index(shuffle, L, index, repeat=1):
    """
    Find origin index using coefficients of complete shuffle
    """
    a, b = reverse_coefficients(shuffle, L, index, repeat)
    return (a * index + b) % L


def code1(n):
    shuffle, length, result = get_data(n)
    stack = list(range(length))
    stack = apply(shuffle, stack)
    if result:
        assert stack == result, (result, stack)
    else:
        index1 = stack.index(2019)
        index2 = forward_index_v1(shuffle, length, 2019)
        index3 = forward_index(shuffle, length, 2019)
        assert index1 == index2 == index3
        print('1>', index1)


def code2(n):
    shuffle, length, result = get_data(n)
    print('---')
    # test backward index on known solution
    n = 2019
    repeat = 1
    index1 = forward_index(shuffle, length, n, repeat)
    index2 = backward_index_v1(shuffle, length, index1, repeat)
    index3 = backward_index(shuffle, length, index1, repeat)
    print('0>', n)
    print('1>', index1)
    print('2>', index2)
    assert n == index2 == index3
    print('---')
    # test coefficient repetition
    n = 2019
    repeat = 101_741_582_076_661
    index1 = forward_index(shuffle, length, n, repeat)
    index2 = backward_index(shuffle, length, index1, repeat)
    print('0>', n)
    print('1>', index1)
    print('2>', index2)
    assert n == index2
    print('---')
    # solve part 2
    print('2>', backward_index(shuffle, length, index=2020, repeat=repeat))


code1(1)
code1(2)
code1(3)
code1(4)
code1(0)
code2(20)
