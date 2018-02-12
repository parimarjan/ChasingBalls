import random
import time
import numpy as np
# import weldnumpy as np
import os
import argparse
from collections import defaultdict

SCALE = 500
size = 2
colour = (0,0,255)
STEP_SIZE = 0.5
# STEP_SIZE = 1
RANDOM_MOVEMENT = False
# NO_CROSSINGS = False
# args.use_pygame = True
import json

parser = argparse.ArgumentParser()
parser.add_argument("-num_balls", "-n", type=int, required=False,
                    default=4, help="number of balls")
parser.add_argument("-start_step_size", "-s", type=float, required=False,
                    default=0.5, help="")
parser.add_argument("-min_step_size", "-m", type=float, required=False,
                    default=0.1, help="")
parser.add_argument("-no_crossing", "-c", type=int, required=False,
                    default=1, help="")
parser.add_argument("-recording_freq", "-r", type=int, required=False,
                    default=50, help="")
parser.add_argument("-use_pygame", "-p", type=int, required=False,
                    default=1, help="")
parser.add_argument("-name", "-name", type=str, required=False,
                    default="test", help="")
args = parser.parse_args()

if args.use_pygame:
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
        
        if args.use_pygame:
            self.circle = pygame.draw.circle(screen, colour, (int(self.pos[0]),
                int(self.pos[1])), size, 0)
        self.following = None

def init(n=4, coords=None):
    '''
    returns n points.
    '''
    points = []
    for i in range(n):
        # print('i at start = ', i)
        if coords:
            points.append(Point(coord=coords[i]))
        else:
            if args.no_crossing:
                # Only add p2 if it doesn't cause crossings with points so far
                num_try = 0
                while True:
                    num_try += 1
                    p2 = Point()
                    if (i <= 1): 
                        # add 2 points always. Third point onwards be careful.
                        points.append(Point())
                        break
                    found_good_point = True
                    # check every point until i.
                    for j in range(i):
                        if (j < 1):
                            continue
                        if (intersect(points[j-1].pos, points[j].pos,
                            points[i-1].pos, p2.pos) and num_try <= 1000):
                            found_good_point = False
                            break 

                    if found_good_point:
                        break

                    # if (intersect(points[i-2].pos, points[i-1].pos,
                        # points[i-1].pos, p2.pos)):
                        # break 

                if (i > 1):
                    points.append(p2)
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

def ccw(A,B,C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

# Return true if line segments AB and CD intersect
def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

def calculate_crossings(points):
    crossings = 0
    for i, p in enumerate(points):
        cur_dist = np.linalg.norm(p.pos - p.following.pos)
        # don't count for crossings
        if (cur_dist <= 3): continue

        for j, _ in enumerate(points):
            if (i == j): continue
            cur_pt = points[i]
            next_pt = points[(i+1) % len(points)]

            cur_pt2 = points[(i+1) % len(points)]
            next_pt2 = points[(i+2) % len(points)]
            
            if intersect(cur_pt.pos, next_pt.pos, cur_pt2.pos, next_pt2.pos):
                crossings += 1

    return crossings

if args.use_pygame:
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()

def total_dist(points):
    cur_dist = 0
    for p in points:
        cur_dist += np.linalg.norm(p.pos - p.following.pos)
    return cur_dist

STEP_SIZE = args.start_step_size
points = init(n=args.num_balls)
crossings = calculate_crossings(points)
print('total crossings = ', crossings)
print('total dist = ', total_dist(points))
i = 0
data = defaultdict(list)

while True:
    if args.use_pygame:
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
        # FFS figure out how to save frames.
        # if i % 100 == 0:
        if True:
            filename = "Snaps/img%04d.png" % i
            pygame.image.save(screen, filename)
        screen.fill(pygame.Color("black"))
        draw_points(points)
        # pygame.display.flip()

    update(points)
    if i % args.recording_freq == 0:
        d = total_dist(points)
        print('{} : {}'.format(i, d))
        crossings = calculate_crossings(points)
        print('crossings = ', crossings)
        data['iter'].append(i)
        data['crossings'].append(crossings)
        data['dist'].append(d)
        # crossings = calculate_crossings(points)
        # print('total crossings = ', crossings)
        if (d < (float(len(points)) * STEP_SIZE)+1):
            print(float(len(points))/STEP_SIZE)
            print('i = ', i)
            print('d = ', d)
            crossings = calculate_crossings(points)
            print('crossings = ', crossings)
            break
    i += 1 
    # if i % 1000 == 0:
        # print(i)
        # print(total_dist(points))
        # if STEP_SIZE > args.min_step_size:
            # STEP_SIZE = STEP_SIZE / 2

# dump data
with open(args.name + '.json', 'w') as f:
    json.dump(data, f)
