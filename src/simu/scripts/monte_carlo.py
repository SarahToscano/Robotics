import math
import random
import matplotlib.pyplot as plt
import time
from PyQt5 import QtCore, QtWidgets
import pyqtgraph as pg

traject = []
trajectp = []
last_particle = 0

#landmarks = [[1.7292, 1.3577], [6.9168, 5.430904], [1.7292, 5.430904], [6.9168, 1.3577]]
landmarks = []
world_x = 8.646010
world_y = 6.78863
p = []
N = 500

x3 = []
y3 = []
x4 = []
y4 = []

class robot:
    def __init__(self, initial):
        if(initial):
            self.x = 0.96066 # initialise with random
            self.y = 0.872823
            self.orientation = 0.0
        else:
            self.x = random.random() + world_x # initialise with random
            self.y = random.random() + world_y
            self.orientation = random.random() * 2.0 * math.pi
       # draw_particles(self.x,self.y,self.orientation)
        self.forward_noise = 0.0
        self.turn_noise = 0.0
        self.sense_noise = 0.0

    def set(self, new_x, new_y, new_orientation):
        if new_x < 0 or new_x >= world_x:
            raise ValueError('X coordinate out of bound')
        if new_y < 0 or new_y >= world_y:
            raise ValueError('Y coordinate out of bound')
        if new_orientation < 0 or new_orientation >= 2 * math.pi:
            raise ValueError('Orientation must be in [0..2pi]')
        self.x = float(new_x)
        self.y = float(new_y)
        self.orientation = float(new_orientation)

    def set_noise(self, new_f_noise, new_t_noise, new_s_noise):
        # makes it possible to change the noise parameters
        # this is often useful in particle filters
        self.forward_noise = float(new_f_noise)
        self.turn_noise = float(new_t_noise)
        self.sense_noise = float(new_s_noise)

    def sense(self):
        Z = []
        for i in range(len(landmarks)):
            dist = math.sqrt((self.x - landmarks[i][0]) ** 2 + (self.y - landmarks[i][1]) ** 2)
            dist += random.gauss(0.0, self.sense_noise)
            Z.append(dist)
        return Z

    def move(self, turn, x_,y_):
        # if forward < 0:
        #     raise ValueError('Robot cant move backwards')


        # turn, and add randomness to the turning command
        orientation = self.orientation + float(turn) + random.gauss(0.0, self.turn_noise)
        orientation %= 2 * math.pi

        # move, and add randomness to the motion command
        #dist = float(forward) + random.gauss(0.0, self.forward_noise)
        x = x_ + random.gauss(0.0, self.forward_noise)
        y = y_ + random.gauss(0.0, self.forward_noise)
        x %= world_x  # cyclic truncate
        y %= world_y

        # set particle
        res = robot(0)
        res.set(x, y, orientation)
        res.set_noise(self.forward_noise, self.turn_noise, self.sense_noise)
        return res

    def Gaussian(self, mu, sigma, x):
        # calculates the probability of x for 1-dim Gaussian with mean mu and var. sigma
        return math.exp(- ((mu - x) ** 2) / (sigma ** 2) / 2.0) / math.sqrt(2.0 * math.pi * (sigma ** 2))

    def measurement_prob(self, measurement):
        # calculates how likely a measurement should be
        prob = 1.0
        for i in range(len(landmarks)):
            dist = math.sqrt((self.x - landmarks[i][0]) ** 2 + (self.y - landmarks[i][1]) ** 2)
            prob *= self.Gaussian(dist, self.sense_noise, measurement[i])
        return prob


def move(myrobot,step,turn,x,y, land, ih):
    global p, landmarks
    landmarks = land
    for rd in range(step):
        orient = turn
        myrobot = myrobot.move((math.pi / 180) * turn, x,y)
        x3.append(myrobot.x)
        y3.append(myrobot.y)
        Z = myrobot.sense()
        p2 = []
        for i in range(N):
            p2.append(p[i].move((math.pi / 180) * turn, x,y))
        p = p2
        # draw_particles(p, myrobot,2,0)
        # given the particle's location, how likely measure it as Z
        w = []

        for i in range(N):
            w.append(p[i].measurement_prob(Z))
        for rob in p:
            prob = rob.measurement_prob(Z)  # Z remains the same
            w.append(prob)
        # resampling particles based on prabability weights
        p3 = []
        index = int(random.random() * N)
        beta = 0
        mw = max(w)

        for i in range(N):
            beta += random.random() * 2 * mw
            while beta > w[index]:
                beta -= w[index]
                index = (index + 1) % N
            p3.append(p[index])
        p = p3
        if(ih != 0):
            x4.append(p[w.index(min(w))].x)
            y4.append(p[w.index(min(w))].y)
        else:
            x4.append(myrobot.x)
            y4.append(myrobot.y)
        draw_particles(p, myrobot,1,p[w.index(min(w))])
    return (p[w.index(min(w))], orient)

def draw_particles(particles,robotpose,drawp,particle_pose):
    global last_particle
    plt.clf()
    
    #plt.scatter(particle_pose.x, particle_pose.y, s=100, color='blue')
    last_particle=particle_pose
        
    
    plt.scatter(last_particle.x, last_particle.y, s=100, color='blue')

    plt.scatter(robotpose.x, robotpose.y, s=100,color='green')

    plt.plot(x3, y3, color='green')
    plt.plot(x4, y4, color='blue')
    # Draw the significant particles
    for i in landmarks:
        plt.plot(i[0], i[1], marker = 'o', markersize = 2.5,markerfacecolor='black', markeredgecolor
          ='black')
    for i in range(0, len(particles), 30):
        plt.plot(particles[i].x, particles[i].y, marker = 'o', markersize = 2.5, markerfacecolor='red',
        markeredgecolor='red',alpha=0.6)
      
    plt.pause(0.000000000000000000000000000000000000001)






def init(myrobot):
  
    plt.title("Robot World ")
    # Set x, y label text.
    plt.xlim(0, world_x)
    plt.ylim(0, world_y)
    plt.xlabel("X")
    plt.ylabel("Y")


    Z = myrobot.sense()

    # initialise randomly guessed particles
    for i in range(N):
        x = robot(0)
        x.set_noise(0.075, 0.075, 1.5)    #0.05 0.05 0.25    
        p.append(x)

    wi=[]
    for i in range(N):
        wi.append(p[i].measurement_prob(Z))
    draw_particles(p,myrobot,1,myrobot)

