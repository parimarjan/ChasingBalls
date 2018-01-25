import random
import time
import pygame
import numpy as np
import os
import math
import statistics

SCALE = 500
size = 2
colour = (0,0,255)
STEP_SIZE = 0.001
# STEP_SIZE = 1
RANDOM_MOVEMENT = False

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

def getradius(points):
	p = points[0]
	return np.linalg.norm(p.following.pos - p.pos)

def ellipse():
	points = []
	center = 200.0
	r1 = 30.0
	r2 = 120.0
	points.append(Point(coord=(center+random.random()*300, center+random.random()*300)))
	points.append(Point(coord=(center+random.random()*300, center+random.random()*300)))
	points.append(Point(coord=(center+random.random()*300, center+random.random()*300)))
	
	for j in range(3):
		idx = (j+1) % 3
		points[j].following = points[idx]
		
	return points
	
def getstats(points):
	distances = []
	for i, p in enumerate(points):
		distances.append(np.linalg.norm(p.following.pos - p.pos))
	
	average = sum(distances)/len(distances)
	std = statistics.stdev(distances)
	return [average, std]
		
	
def getCentroid(points):
	maxX = 0.0
	maxY = 0.0
	minX = 0.0
	minY = 0.0
	for i, p in enumerate(points):
		if i == 0:
			maxX = p.pos[0]
			maxY = p.pos[1]
			minX = p.pos[0]
			minY = p.pos[1]
		if i > 0:
			if p.pos[0] > maxX:
				maxX = p.pos[0]
			if p.pos[0] < minX:
				minX = p.pos[0]
			if p.pos[1] > maxY:
				maxY = p.pos[1]
			if p.pos[1] < minY:
				minY = p.pos[1]
	return [(maxX+minX)/2,(maxY+minY)/2]
	
def getCentroid2(points):
	x = 0.0
	y = 0.0
	for i, p in enumerate(points):
		x = x + p.pos[0]
		y = y + p.pos[1]
	return [x/len(points), y/len(points)]
	
def getdistances(points):

	sum = 0
	n=3
	for i in range(n):
		p = points[i]
		sum = sum + np.linalg.norm(p.following.pos - p.pos)
	return sum

def circle(n=4):

	points = []
	radius = 100.0
	center = 200.0
	for i in range(n):
		points.append(Point(coord=(center+radius*math.cos(2*math.pi*i/n),center+radius*math.sin(2*math.pi*i/n))))
		
	for j in range(n):
		idx = (j+1) % n
		points[j].following = points[idx]
		
	return points

def draw_points(points):
    '''
    @points: list of point objects which need to be drawn on the screen.
    '''
    for p in points:
         p.circle = pygame.draw.circle(screen, colour, (int(p.pos[0]),
             int(p.pos[1])), size, 0)

pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

coords = [ (100.00,200.00), (400.00, 100.00), (200.00,200.00) ]
# coords = [(200.00,200.00), (200.00, 400.00), (400.00, 400.00), (400.00,200.00)]
points = init(n=len(coords), coords=coords)
# points = init()
#points = init(n=3)
numberofpoints = 3
#points = circle(numberofpoints)
#points = ellipse()
file_num = 0
time = 0 
pointb = 0 
truth = 0
init1 = []
init2 = []
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break
    # clock.tick(80)

    # FFS figure out how to save frames.
    # image = cam.get_image()
    # filename = "Snaps/%04d.png" % file_num
    # pygame.image.save(image, filename)


    screen.fill(pygame.Color("black"))
    if (round(time / STEP_SIZE)) % 1000 == 0:
    	if truth == 0:
    		truth = 1
    		init1 = getCentroid(points)
    		init2 = getCentroid2(points)
    
    	pygame.draw.circle(screen, (255,255,0), (int(init1[0]),int(init1[1])), size, 0)
    	pygame.draw.circle(screen, (0,255,255), (int(init2[0]),int(init2[1])), size, 0)
    	cent = getCentroid(points)
    	cent2 = getCentroid2(points)
    	print (cent)
    	print (cent2)
    	#print (getstats(points))
    	pygame.draw.circle(screen, (255,0,0), (int(cent[0]),int(cent[1])), size, 0)
    	pygame.draw.circle(screen, (0,255,0), (int(cent2[0]),int(cent2[1])), size, 0)
    	draw_points(points)
    	pygame.display.flip()
    	#pointafter = getdistances(points)
    	#print (pointb - pointafter)
    	#pointb = pointafter
    update(points)
    time = time + STEP_SIZE

# os.system("avconv -r 8 -f image2 -i Snaps/%04d.png -y -qscale 0 -s 640x480 -aspect 4:3 result.avi")
