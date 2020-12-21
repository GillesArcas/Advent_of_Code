import re
import itertools
from collections import defaultdict


EXEMPLE = 0
if EXEMPLE == 0:
    DATA = '21.txt'
elif EXEMPLE == 1:
    DATA = '21-exemple1.txt'
else:
    assert False


def read_data():
    with open(DATA) as f:
        lines = [line.strip() for line in f.readlines()]
    cand_allergen = dict()
    all_ingredients = set()
    foods = list()

    for line in lines:
        m = re.match(r'([^(]+) \(contains ([^)]+)', line)
        ingredients = m.group(1).split()
        all_ingredients = all_ingredients.union(ingredients)
        allergens = m.group(2).split(', ')
        foods.append((ingredients, allergens))
        for allergen in allergens:
            if allergen not in cand_allergen:
                cand_allergen[allergen] = set(ingredients)
            else:
                cand_allergen[allergen] = cand_allergen[allergen].intersection(set(ingredients))

    all_cand_allergen = set()
    for k,v in cand_allergen.items():
        print(k, v)
        all_cand_allergen = all_cand_allergen.union(v)
    #print(all_ingredients)
    #print(all_cand_allergen)
    not_allergens = all_ingredients - all_cand_allergen
    # print(not_allergens)

    res = 0
    for ingredients, _ in foods:
        for ingredient in ingredients:
            if ingredient in not_allergens:
                res += 1
    print('1>', res)
    print('-' * 20)
    allergen = dict()
    while True:
        for k,v in cand_allergen.items():
            print(k, v)
        for k,v in cand_allergen.items():
            if len(v) == 1:
                print('found', k, v)
                allergen[k] = list(v)[0]
                alle_to_be_removed = k
                ingr_to_be_removed = list(v)[0]
                break
        del cand_allergen[alle_to_be_removed]
        for k,v in cand_allergen.items():
            cand_allergen[k] = {x for x in v if x != ingr_to_be_removed}
        if not cand_allergen:
            break
        print('-' * 20)

    print(allergen)
    ingre = ','.join(allergen[allerg] for allerg in sorted(allergen))
    print('2>', ingre)



def code1():
    rules = read_data()
    return
    #print(rules)
    n = 0
    for and_rule in itertools.product(*rules[:2]):
        print(and_rule)
        n += 1
        if n % 1000000 == 0:
            print(n)
    print(n)


def code2():
    pass


code1()
code2()
