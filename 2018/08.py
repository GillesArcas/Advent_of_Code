DATA = '08.txt'


def get_data():
    with open(DATA) as f:
        data = [int(_) for _ in f.readline().split()]

    return get_tree(data, pointer=0)[0]


def get_tree(data, pointer):
    if pointer >= len(data):
        return [], pointer
    else:
        num_children = data[pointer]
        num_meta = data[pointer + 1]
        children = list()
        pointer += 2
        for _ in range(num_children):
            child, pointer = get_tree(data, pointer)
            children.append(child)
        meta = data[pointer:pointer + num_meta]
        pointer += num_meta
        return [children, meta], pointer


def sum_meta(tree):
    if not tree:
        return 0
    else:
        return sum(tree[1]) + sum(sum_meta(child) for child in tree[0])


def node_value(tree):
    if not tree:
        return 0
    elif not tree[0]:
        return sum(tree[1])
    else:
        nodesum = 0
        for index in tree[1]:
            if index == 0 or index > len(tree[0]):
                pass
            else:
                nodesum += node_value(tree[0][index - 1])
        return nodesum


def code1():
    tree = get_data()
    print('1>', sum_meta(tree))


def code2():
    tree = get_data()
    print('2>', node_value(tree))


code1()
code2()
