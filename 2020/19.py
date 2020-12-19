import re


EXEMPLE = 0
if EXEMPLE == 0:
    DATA = '19.txt'
elif EXEMPLE == 1:
    DATA = '19-exemple1.txt'
elif EXEMPLE == 2:
    DATA = '19-exemple2.txt'
else:
    assert False


def read_data():
    listrules = list()
    messages = list()
    with open(DATA) as f:
        for line in f:
            line = line.strip()
            if not line:
                break
            listrules.append(line)
        for line in f:
            line = line.strip()
            messages.append(line)
    rules = dict()
    for rule in listrules:
        nrule, drule = parse_rule(rule)
        rules[nrule] = drule
    return rules, messages


def parse_rule(rule):
    m = re.match(r'(\d+): (.*)', rule)
    nrule = int(m.group(1))
    reste = m.group(2)
    if m := re.match(r'"(.*)"', reste):
        return nrule, m.group(1)
    else:
        x = list()
        for alt in reste.split('|'):
            x.append([int(_) for _ in alt.split()])
        return nrule, x


def conv_rule(rules, nrule):
    if type(rules[nrule]) == str:
        return rules[nrule]
    else:
        return '(' + '|'.join([conv_seq_rule(rules, seq_rule) for seq_rule in rules[nrule]]) + ')'


def conv_seq_rule(rules, rule):
    return ''.join([conv_rule(rules, xrule) for xrule in rule])


def code1():
    rules, messages = read_data()
    regex = conv_rule(rules, 0) + '$'

    nmatch = 0
    for message in messages:
        m = re.match(regex, message)
        if m:
            nmatch += 1
    print('>', nmatch)


def code2():
    rules, messages = read_data()
    rules[8] = list()
    rules[11] = list()
    for repeat in range(1, 6):
        rules[8].append([42] * repeat)
        rules[11].append([42] * repeat + [31] * repeat)

    regex = conv_rule(rules, 0) + '$'

    nmatch = 0
    for message in messages:
        m = re.match(regex, message)
        if m:
            nmatch += 1
    print('>', nmatch)


code1()
code2()
