import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ani

# анимация частиц
def animate_particles(trajectory, t, speed=1,  dt=0.04, show={}):
    minx = np.min(trajectory[0][0][..., 0])
    maxx = np.max(trajectory[0][0][..., 0])
    miny = np.min(np.array([parts[0][...,1] for parts in trajectory]), axis=(0,1))
    maxy = np.max(np.array([parts[0][...,1] for parts in trajectory]), axis=(0,1))

    fig, ax = plt.subplots(subplot_kw={'aspect':(maxx-minx)/(maxy-miny)})

    m = int((t/speed)/dt)                       # количество кадров
    n = len(trajectory) // m                    # рисоваться будет каждый n-ый кадр
    num = len(trajectory[0][0])                 # число частиц

    if 'membrane' in show:                          
        ax.imshow([trajectory[0][0][...,1][i:i+int(np.sqrt(num))] for i in range(0, num, int(np.sqrt(num)))])
    else:
        ax.set_xlim(left=minx, right=maxx)
        ax.set_ylim(bottom=miny, top=maxy)
        if 'show_string_not' not in show:           # рисовать линию соединяющую точки по порядку
            ax.plot(trajectory[0][0][...,0], trajectory[0][0][...,1])
        if 'show_points' in show:                   # рисовать точки                           
            ax.scatter(trajectory[0][0][...,0], trajectory[0][0][...,1])
        if 'show_arrows' in show:                   # рисовать векторы скорости                          
            plt.quiver(trajectory[0][0][...,0], trajectory[0][0][...,1],
                    trajectory[0][1][...,0], trajectory[0][1][...,1], scale_units='xy', scale=0.5)

    anim = ani.FuncAnimation(fig, update, frames=m, interval=dt*1000, 
                             fargs=(ax, trajectory, n, num, show))
    plt.show()

# обновление кадра
def update(i, ax, tr, n, num, show):
    colcount = 0
    if 'membrane' in show:                                                # мембрана
        ax.images[0].set_array([tr[i*n][0][...,1][j:j+int(np.sqrt(num))] for j in range(0, num, int(np.sqrt(num)))])
    else:
        if 'show_string_not' not in show:                                 # линия
            ax.lines[0].set_xdata(tr[i*n][0][...,0])
            ax.lines[0].set_ydata(tr[i*n][0][...,1])
        if 'show_points' in show:                                         # точки
            ax.collections[0].set_offsets(tr[i*n][0])
            colcount += 1
        if 'show_arrows' in show:                                         # векторы
            ax.collections[colcount].set_offsets(tr[i*n][0])
            ax.collections[colcount].U = tr[i*n][1][...,0]
            ax.collections[colcount].V = tr[i*n][1][...,1]