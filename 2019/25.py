import itertools
import intcode


DATA = '25.txt'


# list of useful items determined by exploring the area manually
ITEMS = 'polygon,easter egg,tambourine,asterisk,mug,jam,klein bottle,cake'.split(',')


# sequence to pick up all items and go just before final room  determined by
# exploring the area manually
INIT_SEQ ='''\
north
west
take mug
west
take easter egg
east
east
south
south
take asterisk
south
west
north
take jam
south
east
north
east
take klein bottle
south
west
take tambourine
west
take cake
east
south
east
take polygon
north
inv
drop asterisk
drop cake
drop easter egg
drop jam
drop klein bottle
drop mug
drop polygon
drop tambourine
inv
'''


def test_items(computer, items):
    """
    used just before last room
    """
    for item in items:
        computer.invalues.extend([ord(c) for c in f'take {item}'] + [10])
    computer.invalues.extend([ord(c) for c in f'east'] + [10])
    for item in items:
        computer.invalues.extend([ord(c) for c in f'drop {item}'] + [10])


def code1():
    with open(DATA) as f:
        strcode = f.readline().strip()
        code = intcode.parse_data(strcode)

    computer = intcode.Intcode(code)
    computer.verbose_output = False
    computer.trace = False

    for line in INIT_SEQ.splitlines():
        computer.invalues.extend([ord(c) for c in line.strip()] + [10])

    items_combinations = list()
    for n in range(1, len(ITEMS) + 1):
        items_combinations.extend(list(itertools.combinations(ITEMS, n)))

    def input_callback():
        if computer.outvalues:
            print(''.join(chr(_) for _ in computer.outvalues))
            computer.outvalues.clear()

        if not computer.invalues:
            if items_combinations:
                items = items_combinations.pop(0)
                test_items(computer, items)
            else:
                inp = input()
                if inp == 'end':
                    exit()
                if inp == 'n':
                    inp = 'north'
                if inp == 'e':
                    inp = 'east'
                if inp == 's':
                    inp = 'south'
                if inp == 'w':
                    inp = 'west'
                computer.invalues.extend([ord(c) for c in inp] + [10])

        return computer.invalues.pop(0)

    while 1:
        computer.run([], input_callback=input_callback, return_output=False, return_input=True)
        if computer.returned_on == 'terminate':
            print(''.join(chr(_) for _ in computer.outvalues))
            break


code1()
