"""
--- Day 7: Camel Cards ---
"""


import re
from operator import itemgetter


EXAMPLES1 = (
    ('07-exemple1.txt', 6440),
)

EXAMPLES2 = (
    ('07-exemple1.txt', 5905),
)

INPUT = '07.txt'


CARDS1 = 'AKQJT98765432'
CARDS2 = 'AKQT98765432J'


def find_type1(hand):
    sorted_hand = ''.join(sorted(list(hand)))

    if re.search(r'(.)\1\1\1\1', sorted_hand):
        return 1
    elif re.search(r'(.)\1\1\1', sorted_hand):
        return 2
    elif re.search(r'(.)\1\1(.)\2', sorted_hand):
        return 3
    elif re.search(r'(.)\1(.)\2\2', sorted_hand):
        return 3
    elif re.search(r'(.)\1\1', sorted_hand):
        return 4
    elif re.search(r'(.)\1.?(.)\2', sorted_hand):
        return 5
    elif re.search(r'(.)\1', sorted_hand):
        return 6
    else:
        return 7


def find_type2(hand):
    type1 = find_type1(hand)
    nJ = sum(_ == 'J' for _ in hand)

    if nJ == 1:
        improv = {1: None, 2: 1, 3: None, 4: 2, 5: 3, 6: 4, 7: 6}
        return improv[type1]
    elif nJ == 2:
        improv = {1: None, 2: None, 3: 1, 4: None, 5: 2, 6: 4, 7: None}
        return improv[type1]
    elif nJ == 3:
        if type1 == 3:
            return 1
        elif type1 == 4:
            return 2
        return type1
    elif nJ == 4:
        return 1
    else:
        return type1


def read_data(filename):
    hands = []
    with open(filename) as f:
        for line in f:
            hand, bid = line.strip().split()
            hands.append([hand, int(bid)])
    return hands


def code1(hands):
    table = str.maketrans(CARDS1, 'ABCDEFGHIJKLM')
    for hand in hands:
        translated_hand = hand[0].translate(table)
        hand.append(find_type1(hand[0]))
        hand.append(translated_hand)
    hands = sorted(hands, key=itemgetter(2, 3), reverse=True)
    return sum(rank * bid for rank, (_, bid, _, _) in enumerate(hands, 1))


def code2(hands):
    table = str.maketrans(CARDS2, 'ABCDEFGHIJKLM')
    for hand in hands:
        hand.append(find_type2(hand[0]))
        hand.append(hand[0].translate(table))
    hands = sorted(hands, key=itemgetter(2, 3), reverse=True)
    return sum(rank * bid for rank, (_, bid, _, _) in enumerate(hands, 1))


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
