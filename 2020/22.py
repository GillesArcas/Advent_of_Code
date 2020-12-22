
EXEMPLE = 0
if EXEMPLE == 0:
    DATA = '22.txt'
elif EXEMPLE == 1:
    DATA = '22-exemple1.txt'
else:
    assert False


def read_data():
    with open(DATA) as f:
        lines = [line.strip() for line in f.readlines()]
    deck1 = [int(_) for _ in lines[1:lines.index('Player 2:') - 1]]
    deck2 = [int(_) for _ in lines[lines.index('Player 2:') + 1:]]
    return deck1, deck2


def code1():
    deck1, deck2 = read_data()
    deck1, deck2 = combat1(deck1, deck2)
    result(deck1, deck2)


def combat1(deck1, deck2):
    while deck1 and deck2:
        card1 = deck1.pop(0)
        card2 = deck2.pop(0)
        if card1 > card2:
            deck1.append(card1)
            deck1.append(card2)
        else:
            deck2.append(card2)
            deck2.append(card1)
    return deck1, deck2


def result(deck1, deck2):
    winner = deck1 or deck2
    print(winner)
    score = 0
    for index, card in enumerate(winner[::-1], 1):
        score += index * card
    print('>', score)


def code2():
    deck1, deck2 = read_data()
    winner, deck1, deck2 = combat2(deck1, deck2)
    result(deck1, deck2)


def combat2(deck1, deck2):
    cache = set()
    while deck1 and deck2:
        key = (tuple(deck1), tuple(deck2))
        if key in cache:
            return 1, deck1, deck2
        else:
            cache.add(key)
        card1 = deck1.pop(0)
        card2 = deck2.pop(0)
        if len(deck1) >= card1 and len(deck2) >= card2:
            winner, _, _ = combat2(deck1[:card1], deck2[:card2])
            if winner == 1:
                deck1.append(card1)
                deck1.append(card2)
            else:
                deck2.append(card2)
                deck2.append(card1)
        else:
            if card1 > card2:
                deck1.append(card1)
                deck1.append(card2)
            else:
                deck2.append(card2)
                deck2.append(card1)
    return 1 if deck1 else 2, deck1, deck2


code1()
code2()
