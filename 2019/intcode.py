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


class Intcode:
    def __init__(self, code):
        """
        code: list of integer instructions
        """
        self.code = code[:]
        self.ptr = 0
        self.relbase = 0
        self.invalues = list()
        self.outvalues = list()
        self.returned_on = None  # 'output' or 'terminate'

    def run(self, initval, return_output=False):
        """
        initval: list of input values
        return_output: return on output if True
        return: last output
        """
        self.invalues.extend(initval)
        while True:
            instr = self.code[self.ptr]
            op = instr % 100
            mode = instr // 100
            #print('loop', self.ptr, instr, op)
            if op == 1:  # add
                i, j, dest = self.code[self.ptr + 1:self.ptr + 4]
                self.code[dest] = self.opval(mode, i, 0) + self.opval(mode, j, 1)
                self.ptr += 4
            elif op == 2:  # mul
                i, j, dest = self.code[self.ptr + 1:self.ptr + 4]
                self.code[dest] = self.opval(mode, i, 0) * self.opval(mode, j, 1)
                self.ptr += 4
            elif op == 3:  # input
                x = self.code[self.ptr + 1]
                self.code[x] = self.invalues.pop(0)
                self.ptr += 2
            elif op == 4:  # output
                x = self.code[self.ptr + 1]
                outval = self.opval(mode, x, 0)
                self.outvalues.append(outval)
                self.ptr += 2
                if return_output:
                    self.returned_on = 'output'
                    if self.outvalues:
                        return self.outvalues[-1]
                    else:
                        return None
            elif op == 5:  # jump-if-true
                test, target = self.code[self.ptr + 1:self.ptr + 3]
                if self.opval(mode, test, 0) != 0:
                    self.ptr = self.opval(mode, target, 1)
                else:
                    self.ptr += 3
            elif op == 6:  # jump-if-false
                test, target = self.code[self.ptr + 1:self.ptr + 3]
                if self.opval(mode, test, 0) == 0:
                    self.ptr = self.opval(mode, target, 1)
                else:
                    self.ptr += 3
            elif op == 7:  # less than
                i, j, dest = self.code[self.ptr + 1:self.ptr + 4]
                if self.opval(mode, i, 0) < self.opval(mode, j, 1):
                    self.code[dest] = 1
                else:
                    self.code[dest] = 0
                self.ptr += 4
            elif op == 8:  # equals
                i, j, dest = self.code[self.ptr + 1:self.ptr + 4]
                if self.opval(mode, i, 0) == self.opval(mode, j, 1):
                    self.code[dest] = 1
                else:
                    self.code[dest] = 0
                self.ptr += 4
            elif op == 99:  # terminate
                self.returned_on = 'terminate'
                if self.outvalues:
                    return self.outvalues[-1]
                else:
                    return None
            else:
                assert False

    def opval(self, mode, val, rank):
        return self.code[val] if (mode // (10 ** rank)) % 10 == 0 else val

