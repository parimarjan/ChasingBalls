import random
import time
import vpython as vp

SCALE = 3

class Point():

    def __init__(self):
        # self.x = random.random()
        # self.y = random.random()
        # self.z = random.random()
        # self.ball = vp.sphere(color = vp.color.green, radius = 0.4)
        self.ball = vp.sphere (color = vp.color.green, radius = 0.4, make_trail=False, retain=200)

        self.ball.mass = 1.0
        self.ball.pos = vp.vector(random.random(), random.random(), random.random())
        self.ball.p = vp.vector(random.random(), random.random(), random.random())
        # self.ball.p = vp.vector (-0.15, -0.23, +0.27)

def init(n=4):
    '''
    returns n points.
    '''
    points = []
    for i in range(n):
        points.append(Point())
    return points

def update(points):
    '''
    '''
    dt = 0.03
    for point in points:
        point.ball.pos = point.ball.pos + (point.ball.p/point.ball.mass)*dt
        # point.ball.pos.x += 0.1
        # if not (side > point.ball.pos.z > -side):
            # print("went outside ZZZZ")
            # point.ball.pos.z = 0

        # if random.random() % 2 == 0:
            # # point.ball.pos.x += SCALE*random.random()
            # point.ball.pos.y += abs(SCALE*random.random())
            # # point.ball.pos.z += abs(SCALE*random.random())
            # point.ball.pos.z = 0
        # else:
            # # point.ball.pos.x -= SCALE*random.random()
            # point.ball.pos.y -= SCALE*random.random()
            # # point.ball.pos.z += abs(1*random.random())
            # point.ball.pos.z = 0

        if not (side > point.ball.pos.x > -side):
            point.ball.p.x = -point.ball.p.x
        if not (side > point.ball.pos.y > -side):
            point.ball.p.y = -point.ball.p.y
        if not (side > point.ball.pos.z > -side):
            point.ball.p.z = -point.ball.p.z
 
points = init()

side = 4.0
thk = 0.3

side = side - thk*0.5 - points[0].ball.radius

while True:
    vp.rate(400)
    update(points)
    # draw_points(points)
