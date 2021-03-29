import re
import collections


DATA = {0: '04.txt', 1: '04-exemple1.txt'}


def get_data(n):

    data = collections.defaultdict(lambda: collections.defaultdict(list))
    with open(DATA[n]) as f:
        lines = sorted(f.readlines())

    guard = None
    for line in lines:
        match = re.match(r'\[1518-(\d\d-\d\d) \d\d:(\d\d)\] (.+)', line)
        day, minute, event = match.groups()
        match = re.search(r'#(\d+)', event)
        if match:
            guard = int(match.group(1))
        else:
            data[guard][day].append(int(minute))
    return data


def code1(n):
    data = get_data(n)

    maxsleep = 0
    maxguard = None
    for guard, days in data.items():
        sleep = 0
        for day, events in days.items():
            for sleeptime, waketime in zip(events[::2], events[1::2]):
                sleep += waketime - sleeptime
        if sleep > maxsleep:
            maxsleep = sleep
            maxguard = guard

    sleep = [0] * 60
    for day, events in data[maxguard].items():
        for sleeptime, waketime in zip(events[::2], events[1::2]):
            for minute in range(sleeptime, waketime):
                sleep[minute] += 1
    maxminute = sleep.index(max(sleep))

    print('1>', maxguard * maxminute, f'({maxguard} x {maxminute})')


def code2(n):
    data = get_data(n)

    maxguard = None
    maxsleep = 0
    maxminute = 0
    for guard, days in data.items():
        sleep = [0] * 60
        for day, events in days.items():
            for sleeptime, waketime in zip(events[::2], events[1::2]):
                for minute in range(sleeptime, waketime):
                    sleep[minute] += 1
            maxsleep_in_day = max(sleep)
            maxminute_in_day = sleep.index(maxsleep_in_day)
        if maxsleep_in_day > maxsleep:
            maxsleep = maxsleep_in_day
            maxminute = maxminute_in_day
            maxguard = guard

    print('2>', maxguard * maxminute, f'({maxguard} x {maxminute})')


code1(0)
code2(0)
