import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ani

# создание частиц-словарей
def generate_particles(num):
    particles = []
    for i in range(num):
        particles.append({
            'id':i,
            'pos':np.array([np.random.rand(1)[0]*2 - 1, np.random.rand(1)[0]*2 - 1]),
            'vel':np.array([0.0, 0.0]),
            'acc':np.array([0.0, 0.0]),
            'mass':1.0,
            'charge':1.0,
            'props':{}
            }
        )
    return particles

# визуализация частиц-словарей
def visualise_particles(particles, title='title', show_vector=True, save_path=None):
    # получение массивов координат и скоростей
    cords = np.array([part['pos'] for part in particles])
    velos = np.array([part['vel'] for part in particles])   
    # рисование точек
    fig, ax = plt.subplots()
    plt.scatter(cords[...,0], cords[...,1], c=[part['mass'] for part in particles],
                cmap='viridis')
    # рисование стрелок
    if show_vector:        
        plt.quiver(cords[...,0], cords[...,1], velos[...,0], velos[...,1])
    # настройка графика
    ax.set_xlim(left=-1.5, right=1.5)
    plt.xlabel('X')
    ax.set_ylim(bottom=-1.5, top=1.5)
    plt.ylabel('Y')
    plt.title(title)

    plt.show()

def process_springs(particles, springs, dt=0.01):
    # расчет пружин
    for spring in springs:
        part1, part2 = particles[spring[0]], particles[spring[1]]       # соединенные частицы
        vec = part2['pos'] - part1['pos']                               # вектор от первой ко второй
        dist = np.sqrt(np.sum(vec**2))                                  # расстояние между ними
        vec = vec/dist                                                  # единичный ветор
        part1['acc'] = (dist - spring[2])*spring[3]*vec/part1['mass']   # расчёт ускорения
        part2['acc'] = -(dist - spring[2])*spring[3]*vec/part2['mass']  # то же
    # расчет частиц    
    for part in particles:
        part['vel'] += part['acc']*dt
        part['pos'] += part['vel']*dt
        

parts = generate_particles(3)
springs = [(0,1,0.5,0.25), (1,2,0.4,0.3),(2,0,1.0,0.6)]
visualise_particles(parts)
for i in range(10000):
    process_springs(parts, springs)
visualise_particles(parts)
