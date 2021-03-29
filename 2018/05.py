import re
import string


DATA = '05.txt'


def react(polymer):
    pairs = '|'.join([a + b + '|' + b + a for a, b in zip(string.ascii_lowercase, string.ascii_uppercase)])
    length = len(polymer)
    while 1:
        polymer = re.sub(pairs, '', polymer)
        if len(polymer) == length:
            return(length)
        else:
            length = len(polymer)


def code1():
    with open(DATA) as f:
        polymer = f.readline().strip()
    print('1>', react(polymer))


def code2():
    with open(DATA) as f:
        polymer = f.readline().strip()
    minlength = len(polymer)
    for c in string.ascii_lowercase:
        polymer2 = re.sub(c, '', polymer, flags=re.I)
        length = react(polymer2)
        if length < minlength:
            minlength = length
    print('2>', minlength)


code1()
code2()
