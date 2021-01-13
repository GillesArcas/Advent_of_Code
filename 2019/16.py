import itertools


DATA = '16.txt'


def pattern(rank):
    base = (0, 1, 0, -1)
    pat = list()
    for p in base:
        pat.extend([p] * rank)
    ipattern = itertools.cycle(pat)
    next(ipattern)
    return ipattern


def apply(signal):
    # signal: list of digits
    r = list()
    for i in range(1, len(signal) + 1):
        #print(i)
        n = sum(s * p for s, p in zip(signal, pattern(i)))
        r.append(abs(n) % 10)
    return r


def code1():
    with open(DATA) as f:
        signal = f.readline().strip()

    signal = [int(digit) for digit in signal]
    for phase in range(1, 11):
        signal = apply(signal)

    print('1>', ''.join(str(d) for d in signal)[:8])
    print(signal)


def code2():
    """
    Given the offset, at each phase, a digit is the sum (mod 10) of the digits
    starting from this digit.
    """
    with open(DATA) as f:
        signal = f.readline().strip()

    offset = int(signal[:7])
    signal = (signal * 10_000)[offset:]
    signal = [int(digit) for digit in signal]

    for phase in range(1, 101):
        for i in range(len(signal) - 2, -1, -1):
            signal[i] = (signal[i + 1] + signal[i]) % 10

    print('2>', ''.join(str(d) for d in signal[:8]))


#code1()
code2()
