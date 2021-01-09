import re
from collections import defaultdict


DATASET = 0
if DATASET == 0:
    DATA = '14.txt'
elif DATASET == 1:
    DATA = '14-exemple1.txt'
elif DATASET == 2:
    DATA = '14-exemple2.txt'
elif DATASET == 3:
    DATA = '14-exemple3.txt'
elif DATASET == 4:
    DATA = '14-exemple4.txt'
elif DATASET == 5:
    DATA = '14-exemple5.txt'
else:
    assert False


class Reaction:
    def __init__(self, result, nb, products):
        self.result = result
        self.nb = nb
        self.products = [(int(nb), product) for nb, product in products]


def read_data(data):
    reactions = dict()
    with open(data) as f:
        for line in f:
            x = re.findall(r'(\d+) ([A-Z]+)', line)
            nb, result = x[-1]
            reaction = Reaction(result, int(nb), x[:-1])
            reactions[result] = reaction
    return reactions


def obtain(reactions, target):
    # products, spare: defaultdict product => nb
    products = defaultdict(int)
    spare = defaultdict(int)
    products['FUEL'] = target


    while True:
        if len(products) == 1 and list(products)[0] == 'ORE':
            return products['ORE']

        # search a product different from ORE
        for product, nb in products.items():
            if product != 'ORE':
                break

        # remove it (product and nb are correctly set)
        del products[product]

        # enough spare
        if spare[product] >= nb:
            spare[product] -= nb
            continue

        # some spare
        if spare[product] > 0:
            nb -= spare[product]
            spare[product] = 0

        # number of times to apply reaction
        if nb % reactions[product].nb == 0:
            nb_reac = nb // reactions[product].nb
            nb_spare = 0
        else:
            nb_reac = nb // reactions[product].nb + 1
            nb_spare = nb_reac * reactions[product].nb - nb

        # add to products the products required to make the chosen product
        for nb2, product2 in reactions[product].products:
            products[product2] += nb2 * nb_reac

        # add extra product to spare
        spare[product] += nb_spare


def code1():
    nb_ore = obtain(read_data(DATA), target=1)
    print('1>', nb_ore)


def code2():
    reactions = read_data(DATA)
    fuel_min = 1_000_000_000_000 // obtain(reactions, target=1)
    fuel_max = 2 * fuel_min

    while True:
        fuel = (fuel_min + fuel_max) // 2
        nb_ore = obtain(reactions, target=fuel)
        if nb_ore <= 1_000_000_000_000:
            fuel_min = fuel
        else:
            fuel_max = fuel
        print(' >', nb_ore, fuel, fuel_min, fuel_max)
        if fuel_max - fuel_min == 1:
            print('2>', fuel_min, obtain(reactions, target=fuel_min))
            break


code1()
code2()
