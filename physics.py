import numpy as np
from animation import *

# создание частиц-массивов со случайными координатами
def generate_particles(num):
    crds = np.random.rand(num,2)*2 - 1
    vlcs = np.zeros((num,2))
    accs = np.zeros((num,2))
    mass = np.ones((num,2))
    return (crds, vlcs, accs, mass, num)

# расчёт движения частиц
def process_particles(parts, springs, dt, fixed, damping=0.0):
    crds, vlcs, accs, mass, num = parts

    # векторы соединяющие частицы и расстояния между ними
    vecs = np.array([np.diff(np.matlib.meshgrid(crds[...,0], crds[...,0]), axis=0)[0], 
                     np.diff(np.matlib.meshgrid(crds[...,1], crds[...,1]), axis=0)[0]])
    dist = np.sqrt(np.sum(vecs**2, axis=0))
    # расчёт ускорения
    accs = -(np.sum(vecs*(1 - springs[0]/(dist + np.identity(num)))*springs[1], axis=2)*dt/mass.T).T * np.matlib.repmat(fixed, 2, 1).T
    # расчёт скоростей и координат
    vlcs = vlcs + accs*dt - damping*vlcs*dt
    crds = crds + vlcs*dt

    return (crds, vlcs, accs, mass, num)

# расчёт траекторий движения частиц за время t
def time_process(parts, springs, dt, t, fixed_points, damping=0.0):
    n = int(t/dt)                               # количество шагов
    trajectory = [parts]
    
    for i in range(n):
        parts = process_particles(parts, springs, dt, np.array([0 if i in fixed_points else 1 for i in range(parts[4])]), damping)
        trajectory.append(parts)

    return trajectory

# расчёт полной механической энергии системы
def total_energy(parts, springs):
    crds, vlcs, mass, = parts[0], parts[1], parts[3]
    # кинетическая энергия
    E_kin = 0.5 * np.sum(mass * vlcs**2)
    
    # потенциальная энергия пружин
    vecs = np.array([np.diff(np.matlib.meshgrid(crds[...,0], crds[...,0]), axis=0)[0], 
                     np.diff(np.matlib.meshgrid(crds[...,1], crds[...,1]), axis=0)[0]])
    dist = np.sqrt(np.sum(vecs**2, axis=0))

    stretch = dist - springs[0]  # растяжение относительно длины покоя
    E_pot = 0.5 * np.sum(springs[1] * stretch**2)
    return E_kin + E_pot

# симуляция колебаний струны
def string(num, length, tense, k, t, math_dt, fixate_edges=True, 
           initial_velocity=300, excited_particle=1, damping=0.0, count_energy=False):
    parts = []
    parts.append(np.array([[i*length/(num-1) - length/2, 0] for i in range(num)]))     # координаты частиц равномерно распределённых по длине струны вдоль оси x
    parts.append(np.zeros((num,2)))                                                    # начальные скорости равны 0
    parts[1][excited_particle][1] = initial_velocity                                   # кроме номера excited_particle слева 
    parts.append(np.zeros((num,2)))                                                    # начальные ускорения равны 0
    parts.append(np.ones((num,2)))                                                     # массы равны 1
    parts.append(num)                                                                  # количество частиц

    # матрица пружин, соединены соседние частицы
    springs = np.array([[[length/(num-1)*tense if i-j == 1 or i-j == -1 else 0.0 for i in range(num)] for j in range(num)],    # длины
                        [[k if i-j == 1 or i-j == -1 else 0.0 for i in range(num)] for j in range(num)]])                      # жёсткости
    
    traj = time_process(parts, springs, math_dt, t, {0, num-1} if fixate_edges else {}, damping)
    
    if count_energy:    # зависимость энергии системы от времени
        energies = [total_energy(state, springs) for state in traj]
        return traj, energies
    else:
        return traj

def generate_membrane(n, spacing, k, tense=1.0, initial_velocity=[0, 300]):
    """Создаёт двумерную сетку NxN частиц"""
    num = n * n
    x = np.linspace(0, spacing * (n-1), n)
    y = np.linspace(0, spacing * (n-1), n)
    xx, yy = np.meshgrid(x, y)
    crds = np.column_stack([xx.ravel(), yy.ravel()])
    vlcs = np.zeros((num, 2))
    vlcs[(num + n)//2] = initial_velocity
    accs = np.zeros((num, 2))
    mass = np.ones((num, 2))
    
    """Создаёт матрицу пружин, соединены соседние точки по горизонтали и вертикали"""
    springs = np.zeros((2, num, num))   
    for i in range(num-1):
        if (i+1)%n != 0:
            springs[0, i, i+1] = spacing*tense
            springs[1, i, i+1] = k
        if i+n < num:
            springs[0, i, i+n] = spacing*tense
            springs[1, i, i+n] = k
    springs[0] = springs[0] + springs[0].T
    springs[1] = springs[1] + springs[1].T

    return [(crds, vlcs, accs, mass, num), springs]                                                   