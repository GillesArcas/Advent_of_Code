import re
from collections import defaultdict


EXEMPLE = 0
if EXEMPLE == 0:
    DATA = '16.txt'
elif EXEMPLE == 1:
    DATA = '16-exemple1.txt'
elif EXEMPLE == 2:
    DATA = '16-exemple2.txt'
else:
    assert False


def read_data():
    rules = list()
    tickets = list()
    with open(DATA) as f:
        for line in f:
            m = re.match(r'([^:]+): (\d+)-(\d+) or (\d+)-(\d+)', line)
            if m:
                rules.append([m.group(1)] + [int(_) for _ in m.groups()[1:]])
            m = re.match(r'\d+', line)
            if m:
                tickets.append([int(_) for _ in line.split(',')])
    return rules, tickets


def check_ticket(rules, ticket):
    scanning_error = 0
    for field in ticket:
        if any(rule[1] <= field <= rule[2] or rule[3] <= field <= rule[4] for rule in rules):
            pass
        else:
            scanning_error += field
    return scanning_error


def code1():
    rules, tickets = read_data()
    print('>', sum(check_ticket(rules, ticket) for ticket in tickets[1:]))


def code2():
    field_index = defaultdict(list)
    index_field = defaultdict(list)
    fail = defaultdict(list)
    rules, tickets = read_data()
    print(len(rules))
    my_ticket = tickets[0]
    valid_nearby_tickets = [ticket for ticket in tickets if check_ticket(rules, ticket) == 0]
    for index, column in enumerate(zip(*valid_nearby_tickets)):
        #print(index, column)
        for field, v1, v2, v3, v4 in rules:
            #print(field, v1, v2, v3, v4)
            if all(v1 <= v <= v2 or v3 <= v <= v4 for v in column):
                field_index[field].append(index)
                index_field[index].append(field)
            else:
                fail[index].append(field)
    for k,v in field_index.items():
        print(k, v)
    for k,v in index_field.items():
        print(k, v)
    for k,v in fail.items():
        print(k, len(v))

    field_index = defaultdict(list)
    while True:
        removed = False
        for k, v in index_field.items():
            if len(v) == 1:
                field = v[0]
                field_index[field] = k
                print('>', k, field)
                for k2, v2 in index_field.items():
                    if field in v2:
                        v2.remove(field)
                removed = True
        if not removed:
            break
    print(field_index)
    sol = 1
    for k, v in field_index.items():
        if k.startswith('departure'):
            sol *= my_ticket[v]
    print('>', sol)



code1()
code2()
