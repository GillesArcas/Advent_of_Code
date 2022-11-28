
EXAMPLES1 = (
)

EXAMPLES2 = (
)

INPUT = '23.txt'


def read_data(data):
    code = []
    with open(data) as f:
        for line in f:
            code.append(line.strip().split())
    return code


class Run1:
    def __init__(self, code):
        self.code = code
        self.pointer = 0
        self.registers = dict()

    def getvalue(self, x):
        if x in 'abcdefghijklmnopqrstuvwxyz':
            if x in self.registers:
                return self.registers[x]
            else:
                return 0
        else:
            return int(x)

    def setvalue(self, x, y):
        if x in 'abcdefghijklmnopqrstuvwxyz':
            self.registers[x] = y
        else:
            assert 0

    def run(self):
        mul_count = 0
        while True:
            instruction = self.code[self.pointer]
            match instruction:
                # rest variable intended to catch annotations
                case ['set', x, y, *rest]:
                    self.setvalue(x, self.getvalue(y))
                case ['sub', x, y, *rest]:
                    self.setvalue(x, self.getvalue(x) - self.getvalue(y))
                case ['mul', x, y, *rest]:
                    self.setvalue(x, self.getvalue(x) * self.getvalue(y))
                    mul_count += 1
                case ['jnz', x, y, *rest]:
                    if self.getvalue(x) != 0:
                        self.pointer += self.getvalue(y)
                        if self.pointer >= len(self.code):
                            break
                        # cancel common pointer incrementation
                        self.pointer -= 1
            self.pointer += 1
        return mul_count


class Run2:
    def __init__(self, code):
        self.code = code
        self.pointer = 0
        self.registers = dict()
        self.registers['a'] = 1

    def getvalue(self, x):
        if x in 'abcdefghijklmnopqrstuvwxyz':
            if x in self.registers:
                return self.registers[x]
            else:
                return 0
        else:
            return int(x)

    def setvalue(self, x, y):
        if x in 'abcdefghijklmnopqrstuvwxyz':
            self.registers[x] = y
        else:
            assert 0

    def run(self):
        while True:
            instruction = self.code[self.pointer]
            # print(self.pointer, instruction, self.registers)
            match instruction:
                # rest variable intended to catch annotations
                case ['set', x, y, *rest]:
                    self.setvalue(x, self.getvalue(y))
                case ['sub', x, y, *rest]:
                    self.setvalue(x, self.getvalue(x) - self.getvalue(y))
                case ['mul', x, y, *rest]:
                    self.setvalue(x, self.getvalue(x) * self.getvalue(y))
                case ['jnz', x, y, *rest]:
                    if self.getvalue(x) != 0:
                        self.pointer += self.getvalue(y)
                        if self.pointer >= len(self.code):
                            break
                        # cancel common pointer incrementation
                        self.pointer -= 1
            self.pointer += 1
        return self.getvalue('h')


def run2_equivalent():
    """
    Count the number of divisible integers
    """
    h = 0
    for b in range(109300, 109300 + 17000 + 1, 17):
        for d in range(2, b):
            if b % d == 0:
                h += 1
                break
    return h


def code1(code):
    return Run1(code).run()


def code2(code):
    # return Run2(code).run() ... intractable
    return run2_equivalent()


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
