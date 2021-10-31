#! /usr/bin/env python3

import matplotlib
# matplotlib.use('Agg')
import sys
import matplotlib.pyplot as plt
import numpy as np
import math
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
#from nmpc.nmpc import *
sys.path.insert(0, 'src/simu/scripts/nmpc')
from nmpc import Nmpc
#from nmpc.calcUsteps import calcUsteps

INTERVALOS = 15
pi = math.pi
Xrefp = 0
Yrefp = 0
TRst = 0
TRsv = 0
TRsw = 0
Xref = 0
Yref = 0
PHIref = 0
Vref = 0
Wref = 0
TRsx = 0
TRsy = 0

# L1, L2 e L3 sao os pesos para cada componente da funcao de custo
# Pesos em linha reta
L1 = 800
L2 = 600
L3 = 0.1

# Pesos na rotacao
L1_rot = 800
L2_rot = 600
L3_rot = 0.1

# x e y pecorrido
x_pecorrido = []
y_pecorrido = []

def OdometryValues(msg):
    global TRsx, TRsy, TRst, TRsv, TRsw
    TRsx = msg.pose.pose.position.x
    TRsy = msg.pose.pose.position.y
    TRst = msg.pose.pose.orientation.z
    # TRst = 2 * math.atan2(msg.pose.pose.orientation.z,
    #                       msg.pose.pose.orientation.w)
    TRsv = msg.twist.twist.linear.x
    TRsw = msg.twist.twist.angular.z

# def VelocityValues(msg):
#     global 
    
def CalcTetaVW(Vx, aX, Vy, aY):
    tetaRef_ = math.atan2(Vy, Vx)
    Vref_ = math.sqrt(pow(Vx, 2)+pow(Vy, 2))
    # if(Vx == 0.0 and Vy == 0.0):
    #     Wref_ = 0
    # else:
    Wref_ = ((Vx*aY)-(Vy*aX))/(pow(Vx, 2)+pow(Vy, 2))
    # return tetaRef_, Vref_, Wref_
    return Vref_, Wref_


def lerArquivo():
    xref = []
    yref = []
    lines = []
    with open('src/simu/mapa/coords1.txt') as f:
        lines = f.readlines()

    num = 0
    i = 0
    for line in lines:
        if (i == 0):
            MAP_X = int(line)
        elif (i == 1):
            MAP_Y = int(line)
        elif (i == 2):
            num = int(line)
        elif(i <= num+2):
            xref.append(10.645*float(line)/MAP_X)
        else:
            yref.append(22.285*(MAP_Y - float(line))/MAP_Y)

        i = i + 1
    return (MAP_X, MAP_Y, num, xref, yref)


rospy.init_node("control_teste")
velPub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
rospy.Subscriber('/odom', Odometry, OdometryValues, queue_size=1)
velMsg = Twist()
# rate = rospy.Rate(0.8)
rate = rospy.Rate(0.8)

mapx = 10.645
mapy = 22.285

MAP_X, MAP_Y, num, xref, yref = lerArquivo() 

Vx = np.diff(xref)
Vx = np.insert(Vx, 0, 0.0, axis=0)
Vy = np.diff(yref)
Vy = np.insert(Vy, 0, 0.0, axis=0)

acelX = np.diff(Vx)
acelX = np.insert(acelX, 0, 0.0, axis=0)
acelY = np.diff(Vy)
acelY = np.insert(acelY, 0, 0.0, axis=0)

print("########## COMECO DA LOCOMOCAO ############")

Vref = 0
Wref = 0

for i in range(len(xref)):
    
    print()

    print(i)
    Xrefp = xref[i]
    Yrefp = yref[i]
    VXrefp = Vx[i]
    VYrefp = Vy[i]

    Vref, Wref = CalcTetaVW(Vx[i], acelX[i], Vy[i], acelY[i])

    velMsg.linear.x, velMsg.angular.z = Nmpc(
            Xrefp, Yrefp, TRsx, TRsy, TRst, TRsv, TRsw, Xref, Yref, PHIref, Vref, Wref, VXrefp, VYrefp, L1, L2, L3)
    

    print("Querendo ir para X =" ,Xrefp ,", Y =" ,Yrefp)
    print("iRobot.x =" ,TRsx ,", iRobot.y =" ,TRsy)
    print("velo.linear.x =" ,velMsg.linear.x ,", velo.angular.z =" ,velMsg.angular.z)
    
    velPub.publish(velMsg)

    rate.sleep()
    

    
    
    print("Chegou no ponto\n\n")
    

