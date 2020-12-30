import itertools
import intcode


DATA = '07.txt'


def try_phase_setting(code, setting):
    # setting = (a, b, c, d, e)
    print(setting)
    inval = 0
    for ampnum in range(5):
        print('amp', ampnum)
        phase = setting[ampnum]
        outval, _, _ = intcode.run_code(code, [phase, inval])
        inval = outval
    return inval


def try_loop_phase_setting(code, setting):
    # setting = (a, b, c, d, e)
    print(setting)
    amp = [None] * 5
    for ampnum in range(5):
        amp[ampnum] = [0, code[:], None]  # ptr, code, last output

    inval = 0
    for loop in itertools.count():
        for ampnum in range(5):
            phase = setting[ampnum]
            code = amp[ampnum][1]
            ptr = amp[ampnum][0]
            ## print('amp', ampnum, code[ptr])
            if code[ptr] == 99:
                if ampnum == 4:
                    return amp[ampnum][2]
            else:
                if loop == 0:
                    outval, code, ptr = intcode.run_code(code, [phase, inval], ptr=ptr, return_output=True)
                else:
                    outval, code, ptr = intcode.run_code(code, [inval], ptr=ptr, return_output=True)
                amp[ampnum][0] = ptr
                amp[ampnum][1] = code
                if outval is not None:
                    ## print('store', ampnum, outval)
                    amp[ampnum][2] = outval
                inval = outval


def code1():
    with open(DATA) as f:
        strcode = f.readline().strip()
        code = intcode.parse_data(strcode)
    maxval = 0
    for phase_setting in itertools.permutations(range(5)):
        maxval = max(maxval, try_phase_setting(code, phase_setting))
    print('1>', maxval)


def code2():
    with open(DATA) as f:
        strcode = f.readline().strip()
        code = intcode.parse_data(strcode)
    maxval = 0
    for phase_setting in itertools.permutations(range(5, 10)):
        maxval = max(maxval, try_loop_phase_setting(code, phase_setting))
    print('2>', maxval)


# code = intcode.parse_data('3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0')
# result = try_phase_setting(code, (4,3,2,1,0))
# assert result == 43210, result

# code = intcode.parse_data('3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0')
# result = try_phase_setting(code, (0,1,2,3,4))
# assert result == 54321, result

# code = intcode.parse_data('3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0')
# result = try_phase_setting(code, (1,0,4,3,2))
# assert result == 65210, result

#code1()

code = intcode.parse_data('3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5')
result = try_loop_phase_setting(code, (9,8,7,6,5))
assert result == 139629729, result

code = intcode.parse_data('3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10')
result = try_loop_phase_setting(code, (9,7,8,5,6))
assert result == 18216, result

code2()
