import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ani

# создание частиц-массивов со случайными координатами
def generate_particles(num):
    crds = np.random.rand(num,2)*2 - 1
    vlcs = np.zeros((num,2))
    accs = np.zeros((num,2))
    mass = np.ones((num,2))
    return (crds, vlcs, accs, mass, num)

# расчёт движения частиц
def process_particles(parts, springs, dt, fixed):
    crds, vlcs, accs, mass, num = parts

    # векторы соединяющие частицы и расстояния между ними
    vecs = np.array([np.diff(np.matlib.meshgrid(crds[...,0], crds[...,0]), axis=0)[0], 
                     np.diff(np.matlib.meshgrid(crds[...,1], crds[...,1]), axis=0)[0]])
    dist = np.sqrt(np.sum(vecs**2, axis=0))
    # расчёт ускорения
    accs = -(np.sum(vecs*(1 - springs[0]/(dist + np.identity(num)))*springs[1], axis=2)*dt/mass.T).T * np.matlib.repmat(fixed, 2, 1).T
    # расчёт скоростей и координат
    vlcs = vlcs + accs*dt
    crds = crds + vlcs*dt

    return (crds, vlcs, accs, mass, num)

# расчёт траекторий движения частиц за время t
def time_process(parts, springs, dt, t, fixed_points):
    n = int(t/dt)                               # количество шагов
    trajectory = [parts]
    
    for i in range(n):
        parts = process_particles(parts, springs, dt, np.array([0 if i in fixed_points else 1 for i in range(parts[4])]))
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


# анимация частиц
def animate_particles(trajectory, t, dt=0.04, show={}):
    minx = np.min(trajectory[0][0][..., 0])
    maxx = np.max(trajectory[0][0][..., 0])
    miny = np.min(np.array([parts[0][...,1] for parts in trajectory]), axis=(0,1))
    maxy = np.max(np.array([parts[0][...,1] for parts in trajectory]), axis=(0,1))

    fig, ax = plt.subplots(subplot_kw={'aspect':(maxx-minx)/(maxy-miny)/2})

    ax.set_xlim(left=minx, right=maxx)
    ax.set_ylim(bottom=miny, top=maxy)

    m = int(t/dt)                               # количество кадров
    n = len(trajectory) // m                    # рисоваться будет каждый n-ый кадр

    if 'show_string_not' not in show:           # рисовать линию соединяющую точки по порядку
        ax.plot(trajectory[0][0][...,0], trajectory[0][0][...,1])
    if 'show_points' in show:                   # рисовать точки                           
        ax.scatter(trajectory[0][0][...,0], trajectory[0][0][...,1])
    if 'show_points' in show:                   # рисовать векторы скорости                          
        plt.quiver(trajectory[0][0][...,0], trajectory[0][0][...,1],
                   trajectory[0][1][...,0], trajectory[0][1][...,1], scale_units='xy', scale=0.5)

    anim = ani.FuncAnimation(fig, update, frames=m, interval=dt*1000, 
                             fargs=(ax, trajectory, n, show))
    plt.show()

# обновление кадра
def update(i, ax, tr, n, show):
    colcount = 0
    if 'show_string_not' not in show:                                 # линия
        ax.lines[0].set_xdata(tr[i*n][0][...,0])
        ax.lines[0].set_ydata(tr[i*n][0][...,1])
    if 'show_points' in show:                                         # точки
        ax.collections[0].set_offsets(tr[i*n][0])
        colcount += 1
    if 'show_points' in show:                                         # векторы
        ax.collections[colcount].set_offsets(tr[i*n][0])
        ax.collections[colcount].U = tr[i*n][1][...,0]
        ax.collections[colcount].V = tr[i*n][1][...,1]

# симуляция колебаний струны
def string(num, length, tense, k, t, math_dt, anim_dt, anim_speed=1, anim_show={}, fixate_edges=True, count_energy=False):
    parts = []
    parts.append(np.array([[i*length/(num-1) - length/2, 0] for i in range(num)]))     # координаты частиц равномерно распределённых по длине струны вдоль оси x
    parts.append(np.zeros((num,2)))                                                    # начальные скорости равны 0
    parts[1][1][1] = 300                                                               # кроме второй слева 
    parts.append(np.zeros((num,2)))                                                    # начальные ускорения равны 0
    parts.append(np.ones((num,2)))                                                     # массы равны 1
    parts.append(num)                                                                  # количество частиц

    # матрица пружин, соединены соседние частицы
    springs = np.array([[[length/(num-1)*tense if i-j == 1 or i-j == -1 else 0.0 for i in range(num)] for j in range(num)],    # длины
                        [[k if i-j == 1 or i-j == -1 else 0.0 for i in range(num)] for j in range(num)]])                      # жёсткости
    
    traj = time_process(parts, springs, math_dt, t, {0, num-1} if fixate_edges else {})
    
    if count_energy:
        energies = []
        for state in traj:
            energies.append(total_energy(state, springs))
        plt.plot(energies)
        plt.xlabel("шаг")
        plt.ylabel("полная энергия")
        plt.title("Сохранение энергии")
        plt.savefig("energy.png")

    animate_particles(traj, t/anim_speed, anim_dt, anim_show)


string(100, 10000, 0.5, 18000, 120, 0.03819, 0.04, anim_speed=6, count_energy=True)
