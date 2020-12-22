import math


DATASET = 10
if DATASET == 0:
    DATA = '13-exemple.txt'
elif DATASET == 1:
    DATA = '13-exemple2.txt'
elif DATASET == 2:
    DATA = '13-exemple3.txt'
elif DATASET == 3:
    DATA = '13-exemple4.txt'
    BORNEMIN = 1000000000
else:
    DATA = '13.txt'
    BORNEMIN = 100000000000000


def code1():
    with open(DATA) as f:
        arrival = int(f.readline())
        ids = f.readline().split(',')
    deltamin = float('inf')
    for id in ids:
        if id != 'x':
            id = int(id)
            n = 1
            while n * id < arrival:
                n += 1
            delta = n * id - arrival
            if delta < deltamin:
                deltamin = delta
                idmin = id
    print(idmin, deltamin, idmin * deltamin)


def search(ids, above):
    ids = ids.split(',')
    coeffs = []
    for deltat, id in enumerate(ids):
        if id != 'x':
            id = int(id)
            coeffs.append((id, deltat))
    coeffs = sorted(coeffs, key=lambda x: x[0], reverse=True)
    print(coeffs)
    coeffs = coeffs[:2]

    n = int(math.floor((above + coeffs[0][1]) // coeffs[0][0]))
    v = coeffs[0][0] * n
    t = v - coeffs[0][1]
    # print(v)
    # assert (t + coeffs[0][1]) % coeffs[0][0] == 0
    # assert (1202161486 + 3) % 1889 == 0
    # assert (1202161486 + coeffs[0][1]) % coeffs[0][0] == 0

    target = above
    trouve = list()
    trouve.append(0)
    while True:
        #print(v)
        if all(((t + dt) % id == 0) for (id, dt) in coeffs[1:]):
            print('>', t, t - trouve[-1])
            trouve.append(t)
            if len(trouve) == 40:
                return t
        v += coeffs[0][0]
        t = v - coeffs[0][1]
        if t > target:
            print(target)
            target += above // 100


def search(ids, above):
    ids = ids.split(',')
    coeffs = []
    for deltat, id in enumerate(ids):
        if id != 'x':
            id = int(id)
            coeffs.append((id, deltat))
    coeffs = sorted(coeffs, key=lambda x: x[0], reverse=True)
    print(coeffs)
    return search2(coeffs)


def search2(seq):
    print(seq)
    if len(seq) == 1:
        return seq[0][0] - seq[0][1]
    else:
        premsol = search2(seq[:-1])
        mul = math.prod(p for (p, d) in seq[:-1])
        while True:
            premsol += mul
            if (premsol + seq[-1][1]) % seq[-1][0] == 0:
                print(seq, premsol)
                return premsol



def code2():
    assert search('7,13,x,x,59,x,31,19', 1000000) == 1068781
    assert search('17,x,13,19', 1000) == 3417
    assert search('67,7,59,61', 100000) == 754018
    assert search('67,x,7,59,61', 100000) == 779210
    assert search('67,7,x,59,61', 1000000) == 1261476
    assert search('1789,37,47,1889', 1000000000) == 1202161486
    search('37,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,41,x,x,x,x,x,x,x,x,x,601,x,x,x,x,x,x,x,x,x,x,x,19,x,x,x,x,17,x,x,x,x,x,23,x,x,x,x,x,29,x,443,x,x,x,x,x,x,x,x,x,x,x,x,13', 
      100000000000000)


#code1()
code2()
