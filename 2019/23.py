import intcode


DATA = '23.txt'


def pop_input(input_stack, num):
    if not input_stack[num]:
        return -1
    else:
        return input_stack[num].pop(0)


def runcode(part):
    with open(DATA) as f:
        strcode = f.readline().strip()
        code = intcode.parse_data(strcode)

    input_stack = [[num] for num in range(50)]
    NAT_X, NAT_Y = None, None

    def make_input_callback(num):
        def input_callback():
            return pop_input(input_stack, num)
        return input_callback

    input_callback = [make_input_callback(num) for num in range(50)]

    computers = list()
    for num in range(50):
        computer = intcode.Intcode(code)
        computer.verbose_output = False
        computer.trace = False
        computers.append(computer)

    print(input_stack)

    while 1:
        for num in range(50):
            # print('---', num, input_stack[num])
            computers[num].run([], input_callback=input_callback[num], return_output=True, return_input=True)
            if computers[num].returned_on == 'output':
                if len(computers[num].outvalues) >= 3:
                    destnum = computers[num].outvalues.pop(0)
                    X = computers[num].outvalues.pop(0)
                    Y = computers[num].outvalues.pop(0)
                    print(num, '-->', destnum, X, Y)
                    if destnum != 255:
                        input_stack[destnum].append(X)
                        input_stack[destnum].append(Y)
                    elif part == 1:
                        print('1>', Y)
                        return
                    else:
                        if all(not _ for _ in input_stack):
                            if Y == NAT_Y:
                                print('2>', Y)
                                return
                            NAT_x, NAT_Y = X, Y
                            input_stack[0].append(X)
                            input_stack[0].append(Y)


runcode(part=1)
runcode(part=2)