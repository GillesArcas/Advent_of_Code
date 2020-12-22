import itertools


if 0:
    DATA = '09-exemple.txt'
    LEN = 5
else:
    DATA = '09.txt'
    LEN = 25


def read_numbers():
    with open(DATA) as f:
        return [int(_) for _ in f.readlines()]


def code1():
    numbers = read_numbers()
    length = LEN
    for i, n in enumerate(numbers[length:], length):
        seq = numbers[i - length:i]
        if all(p + q != n for p, q in itertools.permutations(seq, 2)):
            print(n)
            return n


def code2():
    numbers = read_numbers()
    target = code1()
    print(target)
    length = LEN
    liste = numbers[:numbers.index(target)]
    print(liste)
    for i in range(len(liste)):
        for j in range(i + 1, len(liste)):
            seq = numbers[i:j]
            if sum(seq) == target:
                print(seq[0], seq[-1], min(seq) + max(seq))
                return


code1()
code2()
