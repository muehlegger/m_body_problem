import numpy as np
import scipy.constants as const
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import mpl_toolkits.mplot3d.axes3d as p3

G = const.G

class celestialObject():
    global I
    I = 0
    def __init__(self, X, m, V):
        global I
        I += 1
        self.i = I
        self.X = X
        self.m = m
        self.V = V
        
    def get_acc(self, objects):
        F = np.zeros(self.X.shape)
        objects_ = objects.copy()
        objects_.remove(self)
        for obj in objects_:
            F += G * obj.m * self.m * (obj.X - self.X) / (np.linalg.norm(obj.X - self.X, 2) * np.linalg.norm(obj.X - self.X, 1) + 1e-2)

        return F / self.m
    
    def update_v(self, objects, dt):
        self.V = self.V + 1/2 * self.get_acc(objects) * dt
    
    def update_x(self, objects, dt):
        self.update_v(objects, dt)
        self.X = self.X + self.V * dt
        self.update_v(objects, dt)

fig = plt.figure()
ax = p3.Axes3D(fig)
ax.set_xlim(-500, 500)
ax.set_ylim(-500, 500)
ax.set_zlim(-500, 500)


G = 0.00001
objects = []
objects.append(celestialObject(np.array([0,0,0]), 0.05, np.array([0,0,0])))
line0 = ax.plot(0,0,0)
n = 40
mass = 2
for i in range(1, n):
    position = np.random.normal(0,200, 3)
    speed = np.random.uniform(-0.01,0.01, 3)
    #speed = np.zeros(3)
    objects.append(celestialObject(position, mass, speed))
    globals()[f"line{i}"] = ax.plot(position[0], position[1], position[2])

T = 1000
dt = 1
N = int(T/dt)
A = np.zeros([N, len(objects), len(objects[0].X)])


def calculate(dt):    
    for j, obj in enumerate(objects):
        obj.update_x(objects, dt)
        A[dt,j,:] = obj.X
        try:
            globals()[f"line{j}"][0].set_xdata(A[dt-50:dt,j,0])
            globals()[f"line{j}"][0].set_ydata(A[dt-50:dt,j,1])
            globals()[f"line{j}"][0].set_3d_properties(A[dt-50:dt,j,2])
        except:
            globals()[f"line{j}"].set_xdata(A[dt-50:dt,j,0])
            globals()[f"line{j}"].set_ydata(A[dt-50:dt,j,1])
            globals()[f"line{j}"].set_3d_properties(A[dt-50:dt,j,2])               

    return tuple([globals()[f"line{j}"] for j in range(len(objects))])


animation = FuncAnimation(fig, func=calculate, frames=np.arange(0, T, dt), interval=1)
plt.show()