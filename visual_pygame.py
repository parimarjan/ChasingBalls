import random
import time
import pygame
import numpy as np
import os

SCALE = 500
size = 2
colour = (0,0,255)
STEP_SIZE = 0.5
# STEP_SIZE = 1
RANDOM_MOVEMENT = False
NO_CROSSINGS = False
NUM_POINTS = 20

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

        self.circle = pygame.draw.circle(screen, colour, (int(self.pos[0]),
            int(self.pos[1])), size, 0)
        self.following = None

def init(n=4, coords=None):
    '''
    returns n points.
    '''
    points = []
    for i in range(n):
        print('i at start = ', i)
        if coords:
            points.append(Point(coord=coords[i]))
        else:
            if NO_CROSSINGS:
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
                        print('found good point = ', i)
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
        if (cur_dist <= 7): continue

        for j, _ in enumerate(points):
            if (i == j): continue
            cur_pt = points[i]
            next_pt = points[(i+1) % len(points)]

            cur_pt2 = points[(i+1) % len(points)]
            next_pt2 = points[(i+2) % len(points)]
            
            if intersect(cur_pt.pos, next_pt.pos, cur_pt2.pos, next_pt2.pos):
                crossings += 1

    return crossings


# coords = [(200.00,200.00), (400.00,400.00), (200.00, 400.00), (400.00, 200.00)]
# coords = [(200.00,200.00), (200.00, 400.00), (400.00, 400.00), (400.00,200.00)]
# points = init(n=len(coords), coords=coords)
# points = init()

pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
points = init(n=NUM_POINTS)
i = 0

crossings = calculate_crossings(points)
print('total crossings = ', crossings)

def total_dist(points):
    cur_dist = 0
    for p in points:
        cur_dist += np.linalg.norm(p.pos - p.following.pos)
    return cur_dist

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break
    # FFS figure out how to save frames.
    filename = "Snaps/%04d.png" % i
    pygame.image.save(screen, filename)

    screen.fill(pygame.Color("black"))

    draw_points(points)
    update(points)
    pygame.display.flip()

    i += 1 
    if i % 100 == 0:
        print(i)
        d = total_dist(points)
        print('{} : {}'.format(i, d))
        # crossings = calculate_crossings(points)
        # print('total crossings = ', crossings)
        if (d < 20):
            print('converged')
            print('i = ', i)
            break

        # if (crossings == 0):
            # print('crossings = 0')
            # print('i = ', i)
            # break

    # if i % 1000 == 0 and STEP_SIZE > 0.01:
        # STEP_SIZE = STEP_SIZE / 2
        # print("new STEP SIZE = ", STEP_SIZE)



# os.system("avconv -r 8 -f image2 -i Snaps/%04d.png -y -qscale 0 -s 640x480 -aspect 4:3 result.avi")
