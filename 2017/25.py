import re
from collections import defaultdict


EXAMPLES1 = (
    ('25-exemple1.txt', 3),
)

EXAMPLES2 = (
)

INPUT = '25.txt'


START_PAT = r'Begin in state (\w).\nPerform a diagnostic checksum after (\d+) steps.'

STATE_PAT = r"""
In state (\w):
  If the current value is 0:
    - Write the value (\d).
    - Move one slot to the (\w+).
    - Continue with state (\w).
  If the current value is 1:
    - Write the value (\d).
    - Move one slot to the (\w+).
    - Continue with state (\w)."""


def read_data(data):
    """
    Return start_state, nb_steps, state descriptions
    """
    with open(data) as f:
        s = f.read()

    start_state, nb_steps = re.findall(START_PAT, s)[0]
    matchs = re.findall(STATE_PAT, s)
    states = dict()
    for state, write0, move0, next0, write1, move1, next1 in matchs:
        states[state] = {0: (int(write0), move0, next0), 1: (int(write1), move1, next1)}

    return start_state, int(nb_steps), states


def run(start_state, nb_steps, states):
    tape = defaultdict(int)
    state = start_state
    cursor = 0

    for _ in range(nb_steps):
        write, move, nextstate = states[state][tape[cursor]]
        tape[cursor] = write
        cursor = cursor - 1 if (move == 'left') else cursor + 1
        state = nextstate

    return sum(tape.values())


def code1(machine):
    return run(*machine)


def code2(machine):
    return None


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
