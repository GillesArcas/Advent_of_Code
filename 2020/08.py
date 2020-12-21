if 0:
    DATA = '08-exemple.txt'
else:
    DATA = '08.txt'


def code():
    opcodes = list()
    with open(DATA) as f:
        for line in f:
            instr, value = line.split()
            opcodes.append((instr, int(value)))
    return opcodes


def runcode(opcodes):
    ptr = 0
    acc = 0
    vu = set()
    while True:
        if ptr >= len(opcodes):
            return 'terminate', acc
        if ptr in vu:
            return 'infinie=te', acc
        instr, value = opcodes[ptr]
        vu.add(ptr)
        if instr == 'nop':
            ptr += 1
        if instr == 'jmp':
            ptr += value
        if instr == 'acc':
            acc += value
            ptr += 1


def code1():
    opcodes = code()
    end, acc = runcode(opcodes)
    print(acc)


def code2():
    opcodes = code()
    for ptr, (instr, value) in enumerate(opcodes):
        if instr in ('nop', 'jmp'):
            newinstr = {'nop': 'jmp', 'jmp': 'nop', 'acc': 'acc'}
            opcodes[ptr] = (newinstr[instr], value)
            end, acc = runcode(opcodes)
            if end == 'terminate':
                print(acc)
                return
            else:
                opcodes[ptr] = (instr, value)


code1()
code2()
