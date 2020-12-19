import re
import collections

n = 0
with open('02.txt') as f:
    for line in f:
        m = re.match(r'(\d+)-(\d+) ([a-z]): ([a-z]+)', line)
        nmin = int(m.group(1))
        nmax = int(m.group(2))
        char = m.group(3)
        pw = m.group(4)
        counter = collections.Counter(pw)
        if nmin <= counter[char] <= nmax:
            n += 1
print(n)

n = 0
with open('02.txt') as f:
    for line in f:
        m = re.match(r'(\d+)-(\d+) ([a-z]): ([a-z]+)', line)
        p1 = int(m.group(1)) - 1
        p2 = int(m.group(2)) - 1
        char = m.group(3)
        pw = m.group(4)
        if (pw[p1] == char) != (pw[p2] == char):
            n += 1
print(n)

