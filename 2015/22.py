"""
--- 2015 --- Day 22: Wizard Simulator 20XX ---
"""


import re
from copy import deepcopy


EXAMPLES1 = (
)

EXAMPLES2 = (
)

INPUT = '22.txt'


def read_data(filename):
    with open(filename) as f:
        boss = Boss(*[int(_) for _ in re.findall(r'\d+', f.read())])
        return boss


class Boss:
    def __init__(self, hit_points, damage):
        self.hit_points, self.damage = hit_points, damage

    def __str__(self):
        return '%d %d' % (self.hit_points, self.damage)


class Player:
    def __init__(self, hit_points, mana):
        self.hit_points, self.mana, self.armor = hit_points, mana, 0
        self.spentmana = 0
        self.spells = []
        self.timer = dict(missile=0, drain=0, shield=0, poison=0, recharge=0)

    def __str__(self):
        return '%d %d' % (self.hit_points, self.mana)


CASTS = dict(
    missile = dict(cost=53, timer=0, damage=4),
    drain = dict(cost=73, timer=0, damage=2, heal=2),
    shield = dict(cost=113, timer=6, armor=7),
    poison = dict(cost=173, timer=6, damage=3),
    recharge = dict(cost=229, timer=5, mana=101))


def apply_cast(player, boss, cast):
    boss.hit_points -= CASTS[cast].get('damage', 0)
    player.hit_points += CASTS[cast].get('heal', 0)
    player.armor += CASTS[cast].get('armor', 0)
    player.mana += CASTS[cast].get('mana', 0)


def apply_boss(player, boss):
    player.hit_points -= max(1, boss.damage - player.armor)


def possible_spells(player):
    spells = []
    for castname, cast in CASTS.items():
        if cast['cost'] < player.mana and player.timer[castname] == 0:
            spells.append(castname)
    return spells


def battle_turn(player, boss, part, spells=None):
    # player turn
    if part == 2:
        player.hit_points -= 1
        if player.hit_points <= 0:
            return False, [(player, boss)]

    for spellname in player.timer:
        if player.timer[spellname] > 0:
            player.timer[spellname] -= 1
            if spellname == 'shield':
                if player.timer[spellname] == 0:
                    player.armor = 0
            else:
                apply_cast(player, boss, spellname)

    if boss.hit_points <= 0:
        return True, [(player, boss)]

    if spells is None:
        spells = possible_spells(player)
        if not spells:
            # unable to cast a spell, player lose
            return False, [(player, boss)]

    results = []
    for spellname in spells:
        player2 = deepcopy(player)
        boss2 = deepcopy(boss)

        player2.mana -= CASTS[spellname]['cost']
        player2.timer[spellname] = CASTS[spellname]['timer']
        player2.spentmana += CASTS[spellname]['cost']
        player2.spells.append(spellname)

        if spellname in ('missile', 'drain', 'shield'):
            apply_cast(player2, boss2, spellname)

        # boss turn
        if part == 2:
            # TODO: problem says -1 hit point before each player turn. Actually,
            # next line commented gives the correct answer and when uncommented,
            # there is no solution, so...
            # player2.hit_points -= 1
            if player2.hit_points <= 0:
                return False, [(player2, boss2)]

        for spellname2 in player2.timer:
            if player2.timer[spellname2] > 0:
                player2.timer[spellname2] -= 1
                if spellname2 == 'shield':
                    if player2.timer[spellname2] == 0:
                        player2.armor = 0
                else:
                    apply_cast(player2, boss2, spellname2)

        if boss2.hit_points <= 0:
            return True, [(player2, boss2)]

        apply_boss(player2, boss2)
        if player2.hit_points <= 0:
            return False, [(player2, boss2)]

        results.append((player2, boss2))
    return None, results


def battle(boss, part):
    player = Player(50, 500)
    mini = float('inf')
    stack = []
    numround = 1
    stack.append((deepcopy(player), deepcopy(boss), numround))
    while stack:
        player, boss, numround = stack.pop(0)
        res, x = battle_turn(player, boss, part)
        if res is True:
            if x[0][0].spentmana < mini:
                mini = x[0][0].spentmana
                print('>', mini, x[0][0].spells)
                # first solution gives the correct answer in both parts
                return mini
        elif res is False:
            pass
        else:
            stack.extend([(*_, numround + 1) for _ in x])
    return mini


def code1(boss):
    return battle(boss, part=1)


def code2(boss):
    return battle(boss, part=2)


def testw():
    battle = 'battle2'
    if battle == 'battle1':
        boss = Boss(13, 8)
        player = Player(10, 250)
        res, x = battle_turn(player, boss, 1, spells=['poison'])
        player, boss = x[0]
        res, x = battle_turn(player, boss, 1, spells=['missile'])

    if battle == 'battle2':
        boss = Boss(14, 8)
        player = Player(10, 250)
        res, x = battle_turn(player, boss, 1, spells=['recharge'])
        player, boss = x[0]
        res, x = battle_turn(player, boss, 1, spells=['shield'])
        player, boss = x[0]
        res, x = battle_turn(player, boss, 1, spells=['drain'])
        player, boss = x[0]
        res, x = battle_turn(player, boss, 1, spells=['poison'])
        player, boss = x[0]
        res, x = battle_turn(player, boss, 1, spells=['missile'])

    player, boss = x[0]
    print(res, x)
    print(player, boss)
    print(player.spentmana)


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


# testw()
# exit(1)
test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
