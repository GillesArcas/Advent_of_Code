import copy
from collections import defaultdict


def init_grid():
    grid_serial = 6392
    grid = defaultdict(lambda: defaultdict(int))
    for x in range(1, 301):
        for y in range(1, 301):
            rack_id = x + 10
            power_level = rack_id * y
            power_level += grid_serial
            power_level *= rack_id
            power_level = (power_level % 1000) // 100
            power_level -= 5
            grid[x][y] = power_level
    return grid


def code1():
    grid = init_grid()
    max_fuel = 0
    for x in range(1, 301 - 3):
        for y in range(1, 301 - 3):
            square_fuel = 0
            for xx in range(x, x + 3):
                for yy in range(y, y + 3):
                    square_fuel += grid[xx][yy]
            if square_fuel > max_fuel:
                max_fuel = square_fuel
                best_cell = x, y
    print('1>', best_cell, max_fuel)


def code2():
    grid = init_grid()
    gridcum = copy.deepcopy(grid)

    for x in range(2, 301):
        for y in range(1, 301):
            gridcum[x][y] += gridcum[x - 1][y]

    for x in range(1, 301):
        for y in range(2, 301):
            gridcum[x][y] += gridcum[x][y - 1]

    max_fuel = 0
    for x in range(1, 301):
        for y in range(1, 301):
            for size in range(1, min(300 - x, 300 - y) + 1):
                square_fuel = 0
                square_fuel = (gridcum[x + size - 1][y + size - 1]
                               + gridcum[x - 1][y - 1]
                               - gridcum[x + size - 1][y - 1]
                               - gridcum[x - 1][y + size - 1])
                if square_fuel > max_fuel:
                    max_fuel = square_fuel
                    best_cell = x, y, size

    print('2>', best_cell, max_fuel)


code1()
code2()
