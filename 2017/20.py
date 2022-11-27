import re
from PIL import Image, ImageDraw


EXAMPLES1 = (
    ('20-exemple1.txt', 0),
)

EXAMPLES2 = (
    ('20-exemple2.txt', 1),
)

INPUT = '20.txt'


def read_data(data):
    particles = []
    with open(data) as f:
        for line in f:
            match = re.match(r'p=<\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)>, v=<\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)>, a=<\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)>', line)
            particle = [int(_) for _ in match.group(1, 2, 3, 4, 5, 6, 7, 8, 9)]
            particle += [sum([abs(particle[_]) for _ in range(3)])]
            particles.append(particle)
    return particles


def step(particles):
    for particle in particles:
        for _ in range(3):
            particle[3 + _] += particle[6 + _]
        for _ in range(3):
            particle[0 + _] += particle[3 + _]
        particle[9] = sum([abs(particle[_]) for _ in range(3)])


def remove_collisions(particles):
    positions = dict()
    for index, particle in enumerate(particles):
        coord = tuple(particle[:3])
        if coord not in positions:
            positions[coord] = [index]
        else:
            positions[coord].append(index)

    colliding_particles = set()
    for list_particles in positions.values():
        if len(list_particles) > 1:
            colliding_particles.update(list_particles)

    new_particles = []
    for index, particle in enumerate(particles):
        if index not in colliding_particles:
            new_particles.append(particle)

    return new_particles


def code1(data):
    particles = data
    for _ in range(1000):
        step(particles)

    closest = min(range(len(particles)), key=lambda x:particles.__getitem__(x)[9])
    return closest


def draw_distances(distances):
    image = Image.new('RGB', (1000, 1000))
    draw = ImageDraw.Draw(image)
    plots = list(map(list, zip(*distances)))

    for i, plot in enumerate(plots):
        plot = [(index, 1000 - value) for index, value in enumerate(plot)]
        draw.line(plot, fill=128)

    image.save('20.png')


def code1__(data):
    # same as code1 with trajectory drawing
    particles = data
    distances = []
    distances += [[particle[-1] // 1000 for particle in particles]]
    for _ in range(1000):
        step(particles)
        distances += [[particle[-1] // 1000 for particle in particles]]

    draw_distances(distances)

    closest = min(range(len(particles)), key=lambda x:particles.__getitem__(x)[9])
    return closest


def code2(data):
    particles = data
    for _ in range(1000):
        step(particles)
        particles = remove_collisions(particles)

    return len(particles)


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
