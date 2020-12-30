from collections import Counter


DATA = '08.txt'


def code1():
    with open(DATA) as f:
        data = f.readline().strip()
    dimlayer = 25 * 6
    nblayer = len(data) // dimlayer
    print('nblayer', nblayer)
    min0 = float('inf')
    minprod = None
    for k in range(0, len(data), dimlayer):
        layer = data[k:k + dimlayer]
        counter = Counter(layer)
        if counter['0'] < min0:
            min0 = counter['0']
            minprod = counter['1'] * counter['2']
    print('1>', minprod)


def code2():
    with open(DATA) as f:
        data = f.readline().strip()
    dimlayer = 25 * 6
    nblayer = len(data) // dimlayer
    layers = list()
    for k in range(0, len(data), dimlayer):
        layer = data[k:k + dimlayer]
        layers.append(layer)
    image = list()
    for i in range(dimlayer):
        for layer in layers:
            if layer[i] < '2':
                image.append(layer[i])
                break
    image = ''.join(image)
    for k in range(0, dimlayer, 25):
        print(image[k:k + 25].replace('0', ' ').replace('1', '0'))


code1()
code2()
