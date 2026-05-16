from physics import *
from animation import *

n = 10

parts, springs = generate_membrane(n, 10, 100000)

fixate = set()
for i in range(n):
    fixate.add(i)
    fixate.add(n*n-i)
    fixate.add(i*n)
    fixate.add((i+1)*n-1)
               
traj = time_process(parts, springs, 0.01, 100, fixate)
animate_particles(traj, 100, speed=1, show={'membrane'})
animate_particles(traj, 100, speed=1, show={'show_points', 'show_string_not'})