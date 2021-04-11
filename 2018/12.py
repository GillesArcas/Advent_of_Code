
DATA = """\
####....#...######.###.#...##....#.###.#.###.......###.##..##........##..#.#.#..##.##...####.#..##.#
..... => .
....# => .
...#. => .
...## => #
..#.. => .
..#.# => .
..##. => .
..### => .
.#... => #
.#..# => #
.#.#. => #
.#.## => #
.##.. => .
.##.# => .
.###. => #
.#### => #
#.... => .
#...# => .
#..#. => .
#..## => #
#.#.. => #
#.#.# => #
#.##. => #
#.### => #
##... => #
##..# => .
##.#. => .
##.## => #
###.. => .
###.# => .
####. => .
##### => #
"""


def get_data():
    data = DATA.splitlines()
    pots = data[0]
    rules = dict()
    for line in data[1:]:
        lhs, rhs = line.split(' => ')
        rules[lhs] = rhs
    return pots, rules


def apply_rules(pots, center, rules):
    while not pots.startswith('...'):
        pots = '.' + pots
        center += 1
    while not pots.endswith('...'):
        pots = pots + '.'
    newpots = ['.'] * 2
    for i in range(2, len(pots) - 2):
        newpots.append(rules[pots[i - 2: i - 2 + 5]])
    newpots.extend(['.'] * 2)
    return ''.join(newpots), center


def sumpots(pots, center):
    sumplants = 0
    for num, pot in enumerate(pots, -center):
        if pot == '#':
            sumplants += num
    return sumplants


def run(part, ngen):
    pots, rules = get_data()
    center = 0
    sum0 = sumpots(pots, center)
    for iteration in range(1, ngen + 1):
        pots, center = apply_rules(pots, center, rules)
        #sum1 = sumpots(pots, center)
        #print(iteration, len(pots), sum1, sum1 - sum0)
        #sum0 = sum1
        #print(pots)
    return sumpots(pots, center)


def code1():
    print('1>', run(1, 20))


def code2():
    """
    After step 96, the pattern repeats itself and shift one place on the right.
    Found by tracing patterns and differences between consecutive values.
    """
    #run(2, 200)
    print('2>', 3400 + (50_000_000_000 - 96) * 32)


code1()
code2()
