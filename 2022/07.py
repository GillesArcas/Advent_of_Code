"""
--- 2022 --- Day 7: No Space Left On Device ---
"""


EXAMPLES1 = (
    ('07-exemple1.txt', 95437),
)

EXAMPLES2 = (
    ('07-exemple1.txt', 24933642),
)

INPUT = '07.txt'


class File:
    def __init__(self, genre, name, arg):
        self.genre = genre
        self.name = name
        if self.genre == 'dir':
            self.files = []
            self.parent = arg
        else:
            self.size = arg

    def print(self, indent=0):
        if self.genre == 'dir':
            print(' ' * indent, self.name)
            for file in self.files:
                file.print(indent + 4)
        else:
            print(' ' * indent, self.name, self.size)


def read_data(data):
    with open(data) as f:
        lines = [_.strip() for _ in f.readlines()]

    root = File('dir', '/', None)
    curr = root

    iline = 0
    while iline < len(lines):
        assert lines[iline][0] == '$'
        match lines[iline].split()[1:]:
            case ['cd', directory]:
                if directory == '/':
                    curr = root
                elif directory == '..':
                    curr = curr.parent
                else:
                    curr = [_ for _ in curr.files if _.name == directory][0]
                iline += 1
            case ['ls']:
                iline += 1
                while iline < len(lines) and lines[iline][0] != '$':
                    x, name = lines[iline].split()
                    if x == 'dir':
                        curr.files.append(File('dir', name, curr))
                    else:
                        curr.files.append(File('file', name, int(x)))
                    iline += 1

    return root


def setsizedir(elem):
    if elem.genre == 'dir':
        elem.size = sum(setsizedir(_) for _ in elem.files)
    return elem.size


def total_below(directory):
    if directory.size < 100_000:
        return directory.size + sum(total_below(_) for _ in directory.files if _.genre == 'dir')
    else:
        return sum(total_below(_) for _ in directory.files if _.genre == 'dir')


def all_sizes(directory):
    sizes = [directory.size]
    for subdir in directory.files:
        if subdir.genre == 'dir':
            sizes.extend(all_sizes(subdir))
    return sorted(sizes)


def code1(root):
    setsizedir(root)
    return total_below(root)


def code2(root):
    setsizedir(root)
    sizes = all_sizes(root)
    free = 70000000 - root.size
    for size in sizes:
        if size > 30000000 - free:
            return size


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
