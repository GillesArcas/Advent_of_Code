
EXAMPLES1 = (
    ('18-exemple1.txt', 4),
)

EXAMPLES2 = (
)

INPUT = '18.txt'


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
        while True:
            instruction = self.code[self.pointer]
            match instruction:
                case ['snd', x]:
                    frequency = self.getvalue(x)
                case ['rcv', x]:
                    if self.getvalue(x) == 0:
                        pass
                    else:
                        return frequency
                case ['set', x, y]:
                    self.setvalue(x, self.getvalue(y))
                case ['add', x, y]:
                    self.setvalue(x, self.getvalue(x) + self.getvalue(y))
                case ['mul', x, y]:
                    self.setvalue(x, self.getvalue(x) * self.getvalue(y))
                case ['mod', x, y]:
                    self.setvalue(x, self.getvalue(x) % self.getvalue(y))
                case ['jgz', x, y]:
                    if self.getvalue(x) > 0:
                        self.pointer += self.getvalue(y)
                        # cancel common pointer incrementation
                        self.pointer -= 1
            self.pointer += 1


class Run2:
    def __init__(self, code, program_id):
        self.code = code
        self.pointer = 0
        self.registers = dict()
        self.registers['p'] = program_id
        self.queue = []
        self.send_number = 0

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

    def run(self, other_queue):
        while True:
            instruction = self.code[self.pointer]
            match instruction:
                case ['snd', x]:
                    other_queue.append(self.getvalue(x))
                    self.send_number += 1
                case ['rcv', x]:
                    if self.queue:
                        self.setvalue(x, self.queue.pop(0))
                    else:
                        return
                case ['set', x, y]:
                    self.setvalue(x, self.getvalue(y))
                case ['add', x, y]:
                    self.setvalue(x, self.getvalue(x) + self.getvalue(y))
                case ['mul', x, y]:
                    self.setvalue(x, self.getvalue(x) * self.getvalue(y))
                case ['mod', x, y]:
                    self.setvalue(x, self.getvalue(x) % self.getvalue(y))
                case ['jgz', x, y]:
                    if self.getvalue(x) > 0:
                        self.pointer += self.getvalue(y)
                        # cancel common pointer incrementation
                        self.pointer -= 1
            self.pointer += 1


def code1(code):
    run = Run1(code)
    return run.run()


def code2(code):
    run0 = Run2(code, 0)
    run1 = Run2(code, 1)
    while True:
        run0.run(run1.queue)
        run1.run(run0.queue)
        if not(run0.queue or run1.queue):
            break
    return run1.send_number


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
