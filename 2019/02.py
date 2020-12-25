DATA = '02.txt'


def read_data(data):
    with open(data) as f:
        line = f.readline().strip()
    return [int(_) for _ in line.split(',')]


def run_code(code):
    ptr = 0
    while code[ptr] != 99:
        op, i, j, dest = code[ptr:ptr + 4]
        if op == 1:
            code[dest] = code[i] + code[j]
        elif op == 2:
            code[dest] = code[i] * code[j]
        else:
            assert False
        ptr += 4
    return code


def code1():
    code = read_data(DATA)
    code[1] = 12
    code[2] = 2
    code = run_code(code)
    print('1>', code[0])


def code2():
    code_init = read_data(DATA)
    for i in range(0, 100):
        for j in range(0, 100):
            code = code_init[:]
            code[1] = i
            code[2] = j
            code = run_code(code)
            if code[0] == 19690720:
                break
        else:
            continue
        # break for i only after break for j
        break
    print('2>', code[1] * 100 + code[2])


print(run_code([int(_) for _ in '1,9,10,3,2,3,11,0,99,30,40,50'.split(',')]))
print(run_code([int(_) for _ in '1,1,1,4,99,5,6,0,99'.split(',')]))
code1()
code2()