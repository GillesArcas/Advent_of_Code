import re
import collections


DATA = '07.txt'


def get_data():
    succ = collections.defaultdict(list)
    pred = collections.defaultdict(list)
    with open(DATA) as f:
        for line in f:
            match = re.match(r'Step ([A-Z]) must be finished before step ([A-Z]) can begin.', line)
            succ[match.group(1)].append(match.group(2))
            pred[match.group(2)].append(match.group(1))

    roots = [node for node in succ if not pred[node]]

    return succ, pred, roots


def code1():
    succ, pred, roots = get_data()

    done = list()
    available = sorted(roots)

    while available:
        nextnode = available.pop(0)
        done.append(nextnode)
        available += [node for node in succ[nextnode] if all(_ in done for _ in pred[node])]
        available = sorted(available)

    print('1>', ''.join(done))


def code2():
    succ, pred, roots = get_data()

    done = list()
    available = sorted(roots)
    timing = 0
    workers = [None] * 5

    while available or any(task is not None for task in workers):
        if available and any(task is None for task in workers):
            worker = next(wkr for wkr, task in enumerate(workers) if task is None)
            task = available.pop(0)
            workers[worker] = (task, timing + 60 + ord(task) - ord('A') + 1)
        else:
            soonest = float('inf')
            for worker, data in enumerate(workers):
                if data is not None:
                    task, end_task = data
                    if end_task < soonest:
                        soonest = end_task
                        first_worker_free = worker
                        task_done = task
            timing = soonest
            workers[first_worker_free] = None
            done.append(task_done)
            available += [node for node in succ[task_done] if all(_ in done for _ in pred[node])]
            available = sorted(available)
        # print(done, available, workers)

    print('2>', timing) 


code1()
code2()
