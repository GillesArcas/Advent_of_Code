DATA = '05.txt'


def read_data(data):
    with open(data) as f:
        line = f.readline().strip()
    return parse_data(line)


def parse_data(string):
    return [int(_) for _ in string.split(',')]


def run_code(code, initval):
    ptr = 0
    while code[ptr] != 99:
        instr = code[ptr]
        op = instr % 100
        mode = instr // 100
        #print('loop', instr, op)
        if op == 1:  # add
            i, j, dest = code[ptr + 1:ptr + 4]
            code[dest] = opval(code, mode, i, 0) + opval(code, mode, j, 1)
            ptr += 4
        elif op == 2:  # mul
            i, j, dest = code[ptr + 1:ptr + 4]
            code[dest] = opval(code, mode, i, 0) * opval(code, mode, j, 1)
            ptr += 4
        elif op == 3:  # input
            x = code[ptr + 1]
            code[x] = initval
            ptr += 2
        elif op == 4:  # output
            x = code[ptr + 1]
            outval = opval(code, mode, x, 0)
            print('output', outval)
            ptr += 2
        elif op == 5:  # jump-if-true
            test, target = code[ptr + 1:ptr + 3]
            if opval(code, mode, test, 0) != 0:
                ptr = opval(code, mode, target, 1)
            else:
                ptr += 3
        elif op == 6:  # jump-if-false
            test, target = code[ptr + 1:ptr + 3]
            if opval(code, mode, test, 0) == 0:
                ptr = opval(code, mode, target, 1)
            else:
                ptr += 3
        elif op == 7:  # less than
            i, j, dest = code[ptr + 1:ptr + 4]
            if opval(code, mode, i, 0) < opval(code, mode, j, 1):
                code[dest] = 1
            else:
                code[dest] = 0
            ptr += 4
        elif op == 8:  # equals
            i, j, dest = code[ptr + 1:ptr + 4]
            if opval(code, mode, i, 0) == opval(code, mode, j, 1):
                code[dest] = 1
            else:
                code[dest] = 0
            ptr += 4
        else:
            assert False
    return outval


def opval(code, mode, val, rank):
    return code[val] if (mode // (10 ** rank)) % 10 == 0 else val


def code1():
    run_code(read_data(DATA), initval=1)


def code2():
    assert run_code(parse_data('3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9'), initval=0) == 0
    assert run_code(parse_data('3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9'), initval=9) == 1
    assert run_code(parse_data('3,3,1105,-1,9,1101,0,0,12,4,12,99,1'), initval=0) == 0
    s = '3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99'
    assert run_code(parse_data(s), initval=7) == 999
    assert run_code(parse_data(s), initval=8) == 1000
    assert run_code(parse_data(s), initval=9) == 1001
    run_code(read_data(DATA), initval=5)



# code1()
code2()
