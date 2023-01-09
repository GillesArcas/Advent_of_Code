"""
--- 2015 --- Day 21: RPG Simulator 20XX ---
"""


import re


EXAMPLES1 = (
)

EXAMPLES2 = (
)

INPUT = '21.txt'


def read_data(filename):
    with open(filename) as f:
        boss = Player(*[int(_) for _ in re.findall(r'\d+', f.read())])
        return boss


class Player:
    def __init__(self, hit_points, damage, armor):
        self.hit_points, self.damage, self.armor = hit_points, damage, armor

    def __str__(self):
        return '%d %d %d' % (self.hit_points, self.damage, self.armor)


WEAPONS = dict( #Cost  Damage  Armor
Dagger    =  (  8,     4,       0),
Shortsword=  ( 10,     5,       0),
Warhammer =  ( 25,     6,       0),
Longsword =  ( 40,     7,       0),
Greataxe  =  ( 74,     8,       0))

ARMORS = dict(  #Cost  Damage  Armor
Leather   =  ( 13,     0,       1),
Chainmail =  ( 31,     0,       2),
Splintmail=  ( 53,     0,       3),
Bandedmail=  ( 75,     0,       4),
Platemail =  (102,     0,       5),
No        =  (  0,     0,       0))

RINGS = dict(  #Cost  Damage  Armor
Damage_1  =  ( 25,     1,       0),
Damage_2  =  ( 50,     2,       0),
Damage_3  =  (100,     3,       0),
Defense_1 =  ( 20,     0,       1),
Defense_2 =  ( 40,     0,       2),
Defense_3 =  ( 80,     0,       3),
No        =  (  0,     0,       0))


def battle(player, boss):
    while True:
        boss.hit_points -= max(1, player.damage - boss.armor)
        if boss.hit_points <= 0:
            return player
        player.hit_points -= max(1, boss.damage - player.armor)
        if player.hit_points <= 0:
            return boss


def get_items():
    for weapon in WEAPONS.values():
        for armor in ARMORS.values():
            for ring1 in RINGS.values():
                for ring2 in RINGS.values():
                    if ring1 != ring2:
                        yield (
                            weapon[0] + armor[0] + ring1[0] + ring2[0],
                            weapon[1] + armor[1] + ring1[1] + ring2[1],
                            weapon[2] + armor[2] + ring1[2] + ring2[2]
                        )


def code1(boss):
    boss_hit_points = boss.hit_points
    mini = float('inf')
    for cost, damage, armor in get_items():
        boss.hit_points = boss_hit_points
        if cost < mini:
            player = Player(100, damage, armor)
            if battle(player, boss) == player:
                mini = cost
    return mini


def code2(boss):
    boss_hit_points = boss.hit_points
    maxi = 0
    for cost, damage, armor in get_items():
        boss.hit_points = boss_hit_points
        if cost > maxi:
            player = Player(100, damage, armor)
            if battle(player, boss) == boss:
                maxi = cost
    return maxi


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
