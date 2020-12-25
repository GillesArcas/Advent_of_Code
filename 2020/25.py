
def transform_nbloop(subject, target):
    nbloop = 0
    result = 1
    while True:
        nbloop += 1
        result = (result * subject) % 20201227
        if result == target:
            return nbloop


def transform(subject, nbloop):
    result = 1
    for _ in range(nbloop):
        result = (result * subject) % 20201227
    return result


def encryption_key(card_key, door_key):
    card_loop = transform_nbloop(7, card_key)
    door_loop = transform_nbloop(7, door_key)
    print(card_loop, door_loop)
    print(transform(card_key, door_loop))
    print(transform(door_key, card_loop))
    return transform(card_key, door_loop)


def code1():
    assert encryption_key(5764801, 17807724)
    print('>', encryption_key(16915772, 18447943))


code1()
