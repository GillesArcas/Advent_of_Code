from collections import defaultdict


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
        self.code = defaultdict(int)
        for i, x in enumerate(code):
            self.code[i] = x
        self.ptr = 0
        self.relbase = 0
        self.invalues = list()
        self.outvalues = list()
        self.returned_on = None  # 'output' or 'terminate'
        self.trace = False
        self.verbose_output = True

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
            if self.trace:
                print(self.tracestr())

            if op == 1:  # add
                i, j, dest = self.args(op)
                self.code[self.opdest(mode, dest, 2)] = self.opval(mode, i, 0) + self.opval(mode, j, 1)
                self.ptr += 4

            elif op == 2:  # mul
                i, j, dest = self.args(op)
                self.code[self.opdest(mode, dest, 2)] = self.opval(mode, i, 0) * self.opval(mode, j, 1)
                self.ptr += 4

            elif op == 3:  # input
                dest, = self.args(op)
                self.code[self.opdest(mode, dest, 0)] = self.invalues.pop(0)
                self.ptr += 2

            elif op == 4:  # output
                x, = self.args(op)
                outval = self.opval(mode, x, 0)
                if self.verbose_output:
                    print('output', outval)
                self.outvalues.append(outval)
                self.ptr += 2
                if return_output:
                    self.returned_on = 'output'
                    if self.outvalues:
                        return self.outvalues[-1]
                    else:
                        return None

            elif op == 5:  # jump-if-true
                test, target = self.args(op)
                if self.opval(mode, test, 0) != 0:
                    self.ptr = self.opval(mode, target, 1)
                else:
                    self.ptr += 3

            elif op == 6:  # jump-if-false
                test, target = self.args(op)
                if self.opval(mode, test, 0) == 0:
                    self.ptr = self.opval(mode, target, 1)
                else:
                    self.ptr += 3

            elif op == 7:  # less than
                i, j, dest = self.args(op)
                if self.opval(mode, i, 0) < self.opval(mode, j, 1):
                    self.code[self.opdest(mode, dest, 2)] = 1
                else:
                    self.code[self.opdest(mode, dest, 2)] = 0
                self.ptr += 4

            elif op == 8:  # equals
                i, j, dest = self.args(op)
                if self.opval(mode, i, 0) == self.opval(mode, j, 1):
                    self.code[self.opdest(mode, dest, 2)] = 1
                else:
                    self.code[self.opdest(mode, dest, 2)] = 0
                self.ptr += 4

            elif op == 9:  # relative base
                x, = self.args(op)
                self.relbase += self.opval(mode, x, 0)
                self.ptr += 2

            elif op == 99:  # terminate
                self.returned_on = 'terminate'
                if self.outvalues:
                    return self.outvalues[-1]
                else:
                    return None

            else:
                assert False

    def args(self, op):
        # op is the current opcode
        if op in (1, 2, 7, 8):
            return self.code[self.ptr + 1], self.code[self.ptr + 2], self.code[self.ptr + 3]
        elif op in (5, 6):
            return self.code[self.ptr + 1], self.code[self.ptr + 2]
        elif op in (3, 4, 9):
            return self.code[self.ptr + 1],
        elif op == 99:
            return []
        else:
            assert False

    def opval(self, modes, val, rank):
        mode = (modes // (10 ** rank)) % 10
        if mode == 0:
            return self.code[val]
        elif mode == 1:
            return val
        elif mode == 2:
            return self.code[val + self.relbase]
        else:
            assert False

    def opdest(self, modes, val, rank):
        mode = (modes // (10 ** rank)) % 10
        if mode == 0:
            return val
        elif mode == 2:
            return val + self.relbase
        else:
            assert False

    def tracestr(self):
        instr = self.code[self.ptr]
        op = instr % 100
        return ' '.join(['%04d' % _ for _ in [self.ptr, self.relbase, instr, *self.args(op)]])
