import random
import time
import numpy as np
import os
import argparse

SCALE = 500
size = 2
colour = (0,0,255)
STEP_SIZE = 0.5
# STEP_SIZE = 1
RANDOM_MOVEMENT = False
USE_PYGAME = False

if USE_PYGAME:
    import pygame

def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
       return v
    return v / norm

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
        
        if USE_PYGAME:
            self.circle = pygame.draw.circle(screen, colour, (int(self.pos[0]),
                int(self.pos[1])), size, 0)
        self.following = None

def init(n=4, coords=None):
    '''
    returns n points.
    '''
    points = []
    for i in range(n):
        if coords:
            points.append(Point(coord=coords[i]))
        else:
            points.append(Point())

    # adding the following code.
    for i in range(n):
        idx = (i+1) % n
        points[i].following = points[idx]

    return points

def update(points):
    '''
    '''
    for i, p in enumerate(points):
        # TODO: Normalize this??
        dif = normalize(p.following.pos - p.pos)
        # print("diff = ", dif)
        p.new_pos += dif*STEP_SIZE

        if RANDOM_MOVEMENT:
            if random.randint(0,2) % 2 == 0:
                p.new_pos[0] += SCALE*random.random()
                p.new_pos[1] += SCALE*random.random()
            else:
                p.new_pos[0] -= SCALE*random.random()
                p.new_pos[1] -= SCALE*random.random()
    
    # now that all points positions have been updated, correct pos variable to
    # the new pos.
    for i, p in enumerate(points):
        p.pos = np.copy(p.new_pos)
        # print("for point {}, pos = {}".format(i, p.pos))

def draw_points(points):
    '''
    @points: list of point objects which need to be drawn on the screen.
    '''
    for p in points:
         p.circle = pygame.draw.circle(screen, colour, (int(p.pos[0]),
             int(p.pos[1])), size, 0)

if USE_PYGAME:
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()

# coords = [(200.00,200.00), (400.00,400.00), (200.00, 400.00), (400.00, 200.00)]
# coords = [(200.00,200.00), (200.00, 400.00), (400.00, 400.00), (400.00,200.00)]
# points = init(n=len(coords), coords=coords)
# points = init()
parser = argparse.ArgumentParser()
parser.add_argument("-num_balls", "-n", type=int, required=False,
                    default=4, help="number of balls")
parser.add_argument("-start_step_size", "-s", type=float, required=False,
                    default=0.5, help="")
parser.add_argument("-min_step_size", "-m", type=float, required=False,
                    default=0.1, help="")

args = parser.parse_args()
STEP_SIZE = args.start_step_size
points = init(n=args.num_balls)

i = 0

def total_dist(points):
    cur_dist = 0
    for p in points:
        cur_dist += np.linalg.norm(p.pos - p.following.pos)
    return cur_dist

while True:
    if USE_PYGAME:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
        # FFS figure out how to save frames.
        filename = "Snaps/%04d.png" % i
        pygame.image.save(screen, filename)
        screen.fill(pygame.Color("black"))
        draw_points(points)
        pygame.display.flip()

    update(points)
    i += 1
    if (total_dist(points) < 10):
        print('converged!')
        break


    if i % 1000 == 0:
        print(i)
        print(total_dist(points))
        if STEP_SIZE > args.min_step_size:
            STEP_SIZE = STEP_SIZE / 2
