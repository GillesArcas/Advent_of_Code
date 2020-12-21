import re
from collections import defaultdict


if 0:
    DATA = '07-exemple.txt'
else:
    DATA = '07.txt'


def lines():
    with open(DATA) as f:
        return (_.strip() for _ in f.readlines())


def read_bags1():
    bags = defaultdict(list)
    for line in lines():
        m = re.match(r'(\w+ \w+) bags contain (.*).', line)
        bag = m.group(1)
        if m.group(2) == 'no other bags':
            bags[bag] = []
        else:
            for m in re.finditer(r'(\d+) (\w+ \w+) bag', line):
                bags[bag].append(m.group(2))
    return bags


def read_bags2():
    bags = defaultdict(list)
    for line in lines():
        m = re.match(r'(\w+ \w+) bags contain (.*).', line)
        bag = m.group(1)
        if m.group(2) == 'no other bags':
            bags[bag] = []
        else:
            for m in re.finditer(r'(\d+) (\w+ \w+) bag', line):
                bags[bag].append((int(m.group(1)), m.group(2)))
    return bags


def may_contain(mybag, bagin, bags):
    return mybag in bags[bagin] or any(may_contain(mybag, _, bags) for _ in bags[bagin])


def code1():
    bags = read_bags1()
    print(sum(may_contain('shiny gold', _, bags) for _ in bags))


def contain(bag, bags):
    return sum((n + n * contain(bag2, bags)) for n, bag2 in bags[bag])


def code2():
    bags = read_bags2()
    print(contain('shiny gold', bags))


code1()
code2()
