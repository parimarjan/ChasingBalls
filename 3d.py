import numpy as np
from scipy import integrate

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import cnames
from matplotlib import animation
import random

def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
       return v
    return v / norm

SCALE = 500
STEP_SIZE = 0.1

class Point():
    def __init__(self, dim=2, coord=None):
        self.pos = []
        if coord is None:
            for i in range(dim):
                self.pos.append(SCALE*random.random())
        else:
            for i in range(len(coord)):
                self.pos.append(coord[i])
        
        self.pos = np.array(self.pos)
        self.new_pos = np.copy(self.pos)
        self.following = None

def update(points):
    '''
    '''
    for i, p in enumerate(points):
        # TODO: Normalize this??
        dif = normalize(p.following.pos - p.pos)
        p.new_pos += dif*STEP_SIZE

    
    # now that all points positions have been updated, correct pos variable to
    # the new pos.
    for i, p in enumerate(points):
        p.pos = np.copy(p.new_pos)
        # print("for point {}, pos = {}".format(i, p.pos))

def init2(n=4, coords=None):
    '''
    returns n points.
    '''
    points = []
    for i in range(n):
        if coords:
            points.append(Point(coord=coords[i]))
        else:
            points.append(Point(dim=3))

    # adding the following code.
    for i in range(n):
        idx = (i+1) % n
        points[i].following = points[idx]

    return points

NUM_POINTS = 200
SCALE = 100

# Choose random starting points, uniformly distributed from -15 to 15
np.random.seed(1)

# Set up figure & 3D axis for animation
fig = plt.figure()
ax = fig.add_axes([0, 0, 1, 1], projection='3d')
ax.axis('off')

# choose a different color for each trajectory
colors = plt.cm.jet(np.linspace(0, 1, NUM_POINTS))

# set up lines and points
pts = sum([ax.plot([], [], [], 'o', c=c)
           for c in colors], [])

# prepare the axes limits
ax.set_xlim((-25, 25))
ax.set_ylim((-35, 35))
ax.set_zlim((5, 55))

# set point-of-view: specified by (altitude degrees, azimuth degrees)
ax.view_init(30, 0)

# initialization function: plot the background of each frame
def init():
    for pt in pts:
        pt.set_data([], [])
        pt.set_3d_properties([])
    return pts

# animation function.  This will be called sequentially with the frame number
def animate(i):
    # we'll step two time-steps per frame.  This leads to nice results.
    for i, pt in enumerate(pts):
        update(points)
        x = points[i].pos[0]
        y = points[i].pos[1]
        z = points[i].pos[2]
        pt.set_data(x, y)
        pt.set_3d_properties(z)

    ax.view_init(30, 0.3 * i)
    fig.canvas.draw()
    return pts

points = init2(n=NUM_POINTS)

# instantiate the animator.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=500, interval=1, blit=False)

# anim = animation.FuncAnimation(fig, animate, init_func=init) 
plt.show()
