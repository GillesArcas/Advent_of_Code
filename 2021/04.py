
EXAMPLES1 = (
    ('04-exemple1.txt', 4512),
)

EXAMPLES2 = (
    ('04-exemple1.txt', 1924),
)

INPUT =  '04.txt'


def read_data(fn):
    with open(fn) as f:
        numbers = [int(s) for s in f.readline().strip().split(',')]
        boards = list()
        board = None
        for line in f:
            if not line.strip():
                if board is not None:
                    boards.append(board)
                board = list()
            else:
                board.append([int(s) for s in line.strip().split()])
    return numbers, boards


def test_board(board):
    # True if a row full of 0
    if any(all([n is None for n in line]) for line in board):
        return True
    board = list(map(list, zip(*board)))
    if any(all([n is None for n in line]) for line in board):
        return True
    else:
        return False


def setnumber(board, number):
    for line in board:
        for index, value in enumerate(line):
            if value == number:
                line[index] = None
                return


def code1(data):
    numbers, boards = data
    for number in numbers:
        for board in boards:
            setnumber(board, number)
            if test_board(board):
                return number * sum([sum(0 if n is None else n for n in line) for line in board])
    return 0


def code2(data):
    numbers, boards = data
    count = 0
    done = set()
    for number in numbers:
        for iboard, board in enumerate(boards):
            if iboard in done:
                continue
            setnumber(board, number)
            if test_board(board):
                count += 1
                done.add(iboard)
                # print(iboard, board, number, count, len(boards))
                if count == len(boards):
                    return number * sum([sum(0 if n is None else n for n in line) for line in board])
    return 0


def test(n, code, examples, myinput):
    for fn, result in examples:
        data = read_data(fn)
        assert code(data) == result, (data, result, code(data))

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
