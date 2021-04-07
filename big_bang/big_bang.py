import numpy

def radius_vector(positions):
    vectors = numpy.ndarray((len(positions)))
    for i in range(0, len(positions)):
        vectors[i] = numpy.sqrt(positions[i, 0]**2 + positions[i, 1]**2)
    return vectors

def reverse_time(positions, velocities):
    velocities = -1 * velocities
    t = 0
    min_not_found = 1
    while(min_not_found):
        old_vectors = radius_vector(positions)
        positions = positions + velocities
        new_vectors = radius_vector(positions)
        t = t + 1
        if sum(new_vectors) >= sum(old_vectors):
            min_not_found = 0
            return t - 1

def check_for_collision(positions, velocities, limit, collisions):
    for i in range(0, len(positions)):
        if positions[i, 0] >= limit:
            collisions[i] += 1
            velocities[i, 0] = -1 * velocities[i, 0]
            positions[i, 0] = limit + velocities[i, 0]
        if positions[i, 0] <= -limit:
            collisions[i] += 1
            velocities[i, 0] = -1 * velocities[i, 0]
            positions[i, 0] = -limit + velocities[i, 0]
        if positions[i, 1] >= limit:
            collisions[i] += 1
            velocities[i, 1] = -1 * velocities[i, 1]
            positions[i, 1] = limit + velocities[i, 1]
        if positions[i, 1] <= -limit:
            collisions[i] += 1
            velocities[i, 1] = -1 * velocities[i, 1]
            positions[i, 1] = -limit + velocities[i, 1]
    return positions, velocities, collisions

def normal_time(positions, velocities, timesteps, limit, collisions):
    positions, velocities, collisions = check_for_collision(positions, velocities, limit, collisions)
    for _ in range(0, timesteps):
        positions = positions + velocities
        positions, velocities, collisions = check_for_collision(positions, velocities, limit, collisions)
    return collisions

n, s, t, p = input().split()

n = int(n)
s = int(s)
t = int(t)
p = float(p)

starting_positions = numpy.ndarray((n, 2), dtype=float)
starting_velocities = numpy.ndarray((n, 2), dtype=float)
num_coll = numpy.zeros((len(starting_velocities)))

for i in range(0, n):
    starting_positions[i, 0], starting_positions[i, 1], starting_velocities[i, 0], starting_velocities[i, 1] = input().split()

Ta = reverse_time(starting_positions, starting_velocities)
num_coll = normal_time(starting_positions, starting_velocities, t, s, num_coll)
Tb = int(sum(num_coll))
Tc = p * sum(num_coll/t)

print(Ta, Tb, Tc)
