"""
--- 2018 --- Day 24: Immune System Simulator 20XX ---
"""


import re
import copy


EXAMPLES1 = (
    ('24-exemple1.txt', 5216),
)

EXAMPLES2 = (
    ('24-exemple1.txt', 51),
)

INPUT = '24.txt'


class Group:
    def __init__(self, side, num, nbunits, hitpoints, attack, damage, initiative, weakness, immunity):
        self.side       = side
        self.num        = num
        self.nbunits    = nbunits
        self.hitpoints  = hitpoints
        self.attack     = attack
        self.damage     = damage
        self.initiative = initiative
        self.weakness   = weakness
        self.immunity   = immunity

    def effective_power(self):
        return self.nbunits * self.damage

    def __str__(self):
        return f'{self.side.capitalize()} group {self.num} contains {self.nbunits} units with {self.effective_power()} effective power'


PAT = r'(\d+) units each with (\d+) hit points (?:\(([a-z ,;]+)\) )?with an attack that does (\d+) ([a-z]+) damage at initiative (\d+)'


def read_groups(strdata, side):
    groups = []
    for num, (nbunits, hitpoints, str_weak_imm, damage, attack, initiative) in enumerate(re.findall(PAT, strdata), 1):
        if match := re.search('weak to ([a-z ,]*)(?:;|$)', str_weak_imm):
            weakness = re.findall(r'(\w+)', match.group(1))
        else:
            weakness = []
        if match := re.search('immune to ([a-z ,]*)(?:;|$)', str_weak_imm):
            immunity = re.findall(r'(\w+)', match.group(1))
        else:
            immunity = []

        group = Group(side, num, int(nbunits), int(hitpoints), attack, int(damage), int(initiative), weakness, immunity)
        groups.append(group)
    return groups


def read_data(filename):
    with open(filename) as f:
        data = f.read()

    data_imm = re.findall(r'Immune System:\n(.*)(?:\n\n)|$', data, flags=re.DOTALL)[0]
    data_inf = re.findall(r'Infection:\n(.*)(?:(?:\n\n)|$)', data, flags=re.DOTALL)[0]
    groups_immunity = read_groups(data_imm, 'immunity')
    groups_infection = read_groups(data_inf, 'infection')

    return groups_immunity, groups_infection


def effective_damage(attacker, defender):
    if attacker.attack in defender.immunity:
        damage = 0
    elif attacker.attack in defender.weakness:
        damage = attacker.effective_power() * 2
    else:
        damage = attacker.effective_power()
    return damage


def target_selection(attackers, defenders, fights):
    attackers = sorted(attackers, reverse=True, key=lambda group: (group.effective_power(), group.initiative))
    for attacker in attackers:
        defenders = sorted(defenders, reverse=True,
                       key=lambda group: (effective_damage(attacker, group), group.effective_power(), group.initiative))
        if defenders and effective_damage(attacker, defenders[0]) > 0:
            defender = defenders.pop(0)
            fights.append((attacker, defender))


def attacking_phase(groups_immunity, groups_infection, fights):
    fights = sorted(fights, reverse=True, key=lambda x: x[0].initiative)

    for attacker, defender in fights:
        damage = effective_damage(attacker, defender)
        killed = min(defender.nbunits, damage // defender.hitpoints)
        defender.nbunits = defender.nbunits - killed

        if defender.nbunits == 0:
            if defender in groups_immunity:
                groups_immunity.remove(defender)
            else:
                groups_infection.remove(defender)


def run_fights(data):
    groups_immunity, groups_infection = data
    groups_immunity = copy.deepcopy(groups_immunity)
    groups_infection = copy.deepcopy(groups_infection)
    while True:
        fights = []
        target_selection(groups_immunity, groups_infection, fights)
        target_selection(groups_infection, groups_immunity, fights)
        attacking_phase(groups_immunity, groups_infection, fights)

        if not fights:
            return None, 0
        elif not groups_immunity:
            return 'infection', sum(group.nbunits for group in groups_infection)
        elif not groups_infection:
            return 'immunity', sum(group.nbunits for group in groups_immunity)


def code1(data):
    _, total = run_fights(data)
    return total


def code2(data):
    groups_immunity, _ = data
    for _ in range(1_000_000):
        for group in groups_immunity:
            group.damage += 1
        winner, total = run_fights(data)
        if winner == 'immunity':
            return total


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
