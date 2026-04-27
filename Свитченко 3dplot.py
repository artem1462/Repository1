import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d as mplot3d
import matplotlib.colors as clrs
from matplotlib import cm
import matplotlib.animation as ani
import csv
import json
import pickle
import h5py

def first():
    n = 100
    x = np.linspace(-np.pi, np.pi, num=n)
    y = np.linspace(-np.pi, np.pi, num=n)
    x, y = np.meshgrid(x, y)
    z = np.sin(x)*np.sin(y)

    fig, ax = plt.subplots(subplot_kw={'projection':'3d', 'title':'surface'})
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    surf = ax.plot_surface(x, y, z, cmap=cm.hot)
    fig.show()

    with open('csvfile.csv',  mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=' ', quotechar='|')
        writer.writerow([n])
        writer.writerows(x)
        writer.writerows(y)
        writer.writerows(z)

def second():
    n = 1000
    t = np.linspace(0, 12*np.pi, num=n)
    x = t*np.cos(t)
    y = t*np.sin(t)
    z = t

    fig, ax = plt.subplots(subplot_kw={'projection':'3d', 'title':'trajectory'})
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.view_init(roll=30)
    plot = ax.plot3D(x, y, z)
    fig.show()

    with open('jsonfile.json', mode='w') as file:
        json.dump({'x':list(x), 'y':list(y),
                   'z':list(z)}, file, indent=4)

def third():   
    x = np.linspace(-2, 2, num=5)
    y = np.linspace(-2, 2, num=5)
    z = np.linspace(-2, 2, num=5)
    x, y, z = np.meshgrid(x, y, z)

    fig, ax = plt.subplots(subplot_kw={'projection':'3d', 'title':'vector field'})
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    field = ax.quiver(x, y, z, -y, x, z, length=0.25)
    fig.show()

    with h5py.File('h5pyfile.hdf5', mode='w') as file:
        file.create_dataset('x', data=x)
        file.create_dataset('y', data=y)
        file.create_dataset('z', data=z)

def fourth():
    x = np.linspace(-2, 2, num=100)
    y = np.linspace(-2, 2, num=100)
    x, y = np.meshgrid(x, y)
    z1 = x*x + y*y
    z2 = 5 - x*x - y*y

    fig, ax = plt.subplots(subplot_kw={'projection':'3d', 'title':'surfaces'})
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    surf1 = ax.plot_surface(x, y, z1, cmap=cm.hot)
    surf2 = ax.plot_surface(x, y, z2, cmap=cm.cool)
    fig.show()

    with open('picklefile.pickle', mode='wb') as file:
        pickle.dump({'x':x, 'y':y, 'z1':z1, 'z2':z2}, file)


def fifth():
    n = 20
    r = 1
    phi = np.linspace(0, 2*np.pi, n)
    theta = np.linspace(-np.pi/2, np.pi/2, n)
    x = np.zeros((n, n))
    y = np.zeros((n, n))
    z = r*np.sin(theta)
    z = np.meshgrid(z, z)[0]
    for i in range(n):
        x[i] = r*np.cos(phi[i])*np.cos(theta)
        y[i] = r*np.sin(phi[i])*np.cos(theta)

    fig, ax = plt.subplots(subplot_kw={'projection':'3d', 'title':'sphere',
                                       'box_aspect':(1.,1.,1.)})
    ax.set_xlabel('x')
    ax.set_xlim(left=-1, right=1)
    ax.set_ylabel('y')
    ax.set_ylim(bottom=-1, top=1)
    ax.set_zlabel('z')
    ax.set_zlim(bottom=-1, top=1)
    ax.plot_surface(x, y, z)

    ax.view_init(azim=0)
    def update(i):
        ax.view_init(azim=i)

    anim = ani.FuncAnimation(fig, update, frames = 360, interval=10)
    fig.show()

def readcsv():
    n = 0
    with open('csvfile.csv',  mode='r', newline='') as file:
        n = int(file.readline())

    file = np.loadtxt('csvfile.csv', delimiter=' ', skiprows=1)
    x = np.array(file[0:n])
    y = np.array(file[n:2*n])
    z = np.array(file[2*n:3*n])
    
    fig, ax = plt.subplots(subplot_kw={'projection':'3d', 'title':'surface'})
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    surf = ax.plot_surface(x, y, z, cmap=cm.hot)
    fig.show()

def readjson():
    x = []
    y = []
    z = []
    with open('jsonfile.json', mode='r') as file:
        data = json.load(file)
        x = np.array(data['x'])
        y = np.array(data['y'])
        z = np.array(data['z'])

    fig, ax = plt.subplots(subplot_kw={'projection':'3d', 'title':'trajectory'})
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.view_init(roll=30)
    plot = ax.plot3D(x, y, z)
    fig.show()

def readhdf5():
    x = []
    y = []
    z = []
    with h5py.File('h5pyfile.hdf5', mode='r') as file:
        x = file['x'][:]
        y = file['y'][:]
        z = file['z'][:]

    fig, ax = plt.subplots(subplot_kw={'projection':'3d', 'title':'vector field'})
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    field = ax.quiver(x, y, z, -y, x, z, length=0.25)
    fig.show()

def readpickle():
    x = []
    y = []
    z1 = []
    z2 = []
    with open('picklefile.pickle', mode='rb') as file:
        data = pickle.load(file)
        x = data['x']
        y = data['y']
        z1 = data['z1']
        z2 = data['z2']

    fig, ax = plt.subplots(subplot_kw={'projection':'3d', 'title':'surfaces'})
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    surf1 = ax.plot_surface(x, y, z1, cmap=cm.hot)
    surf2 = ax.plot_surface(x, y, z2, cmap=cm.cool)
    fig.show()

