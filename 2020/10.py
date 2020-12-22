import functools


DATASET = 2
if DATASET == 0:
    DATA = '10-exemple1.txt'
elif DATASET == 1:
    DATA = '10-exemple2.txt'
else:
    DATA = '10.txt'


def read_numbers():
    with open(DATA) as f:
        return [int(_) for _ in f.readlines()]


def code1():
    adapters = sorted(read_numbers())
    adapters = [0, *adapters, max(adapters) + 3]
    diff = [0] * 4
    for p, q in zip(adapters[:-1], adapters[1:]):
        diff[q - p] += 1
    for i, n in enumerate(diff):
        print(i,n)
    print(diff[1] * diff[3])


def nombre_sequences(sequence):
    @functools.lru_cache()
    def nombre_seq(start):
        seq = sequence[start:]
        if len(seq) <= 3:
            return 1
        else:
            nseq = 0
            if seq[1] - seq[0] <= 3:
                nseq += nombre_seq(start + 1)
            if seq[2] - seq[0] <= 3:
                nseq += nombre_seq(start + 2)
            if seq[3] - seq[0] <= 3:
                nseq += nombre_seq(start + 3)
        return nseq
    return nombre_seq(0)


def code2():
    adapters = sorted(read_numbers())
    adapters = [0, *adapters, max(adapters) + 3]
    print(nombre_sequences(adapters))


code1()
code2()
