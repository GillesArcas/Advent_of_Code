import itertools

numbers = list()
with open('01.txt') as f:
    for line in f:
        numbers.append(int(line))

for p, q in itertools.permutations(numbers, 2):
    if p + q == 2020:
        print(p * q)
        break

for p, q, r in itertools.permutations(numbers, 3):
    if p + q + r == 2020:
        print(p * q * r)
        break

