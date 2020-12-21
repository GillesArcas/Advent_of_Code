from collections import Counter

def answers():
    with open('06.txt') as f:
        lines = (_.strip() for _ in f.readlines())
    s = ''
    for line in lines:
        if not line:
            yield s
            s = ''
        else:
            s += ' ' + line
    if s:
        yield s


def code1():
    tot = 0
    for x in answers():
        counter = Counter(x)
        del counter[' ']
        print(x, len(counter), counter)
        tot += len(counter)
    print(tot)


def code2():
    tot = 0
    for x in answers():
        counter = Counter(x)
        t = 0
        for q, n in counter.items():
            if q != ' ' and n == counter[' ']:
                t += 1
        tot += t
        print(x, counter, t)
    print(tot)



code2()
