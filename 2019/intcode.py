def parse_data(string):
    return [int(_) for _ in string.split(',')]


def run_strcode(strcode, initval, ptr=0, return_output=False):
    """
    strcode: comma separated string code
    initval: list of input values
    return_output: return on output if True
    return: last output, code, ptr
    """
    code = parse_data(strcode)
    return run_code(code, initval, return_output)


def run_code(code, initval, ptr=0, return_output=False):
    """
    code: list of integer instructions
    initval: list of input values
    return_output: return on output if True
    return: last output, code, ptr (ptr on next instruction if return_output is True
    """
    print('run', initval)
    ptr = ptr
    outval = None
    while True:
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
            print(initval)
            x = code[ptr + 1]
            code[x] = initval.pop(0)
            ptr += 2
        elif op == 4:  # output
            x = code[ptr + 1]
            outval = opval(code, mode, x, 0)
            print('output', outval)
            ptr += 2
            if return_output:
                print('return_output', outval)
                return outval, code, ptr
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
        elif op == 99:  # terminate
            ## print('terminate', outval)
            return outval, code, ptr
        else:
            assert False


def opval(code, mode, val, rank):
    return code[val] if (mode // (10 ** rank)) % 10 == 0 else val


