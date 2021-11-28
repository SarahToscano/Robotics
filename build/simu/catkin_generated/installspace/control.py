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
import pandas as pd

#localizacao
sys.path.insert(0, 'src/simu/scripts')
from monte_carlo import robot, init, move

#controle
sys.path.insert(0, 'src/simu/scripts/nmpc')
from nmpc import Nmpc
from diffAngle import diffAngle
#from nmpc.calcUsteps import calcUsteps

INTERVALOS = 5
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
L1 = 800 #10
L2 = 500 #2000
L3 = 0.05 


#imagem em pixel
MAP_X = 450
MAP_Y = 360

def OdometryValues(msg):
    global TRsx, TRsy, TRst, TRsv, TRsw
    TRsx = msg.pose.pose.position.x
    TRsy = msg.pose.pose.position.y
    #TRst = msg.pose.pose.orientation.z
    TRst = 2 * math.atan2(msg.pose.pose.orientation.z,
                          msg.pose.pose.orientation.w)
    TRsv = msg.twist.twist.linear.x
    TRsw = msg.twist.twist.angular.z

    
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
    x = []
    y = []
    lines = []
    with open('src/simu/mapa/route.txt') as f:
        lines = f.readlines()

    num = 0
    i = 0
    for line in lines:
        if (i == 0):
            num = int(line)
        else:
            xy = line.split()
            x.append(8.646010*float(xy[0])/MAP_X)
            y.append(6.78863*(float(xy[1]))/MAP_Y)

        i = i + 1
    return (num, x, y)

#localizacao
myrobot = robot(1)
init(myrobot)

rospy.init_node("control_teste")
velPub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
rospy.Subscriber('/odom', Odometry, OdometryValues, queue_size=1)
velMsg = Twist()
# rate = rospy.Rate(0.8)
rate = rospy.Rate(1.6)

xref = []
yref = [] 
num, x, y = lerArquivo()


for i in range(len(x) - 1):
    inter = np.linspace(x[i], x[i+1], INTERVALOS)
    for j in range(1, len(inter)):
        xref.append(inter[j])
    inter = np.linspace(y[i], y[i+1], INTERVALOS)
    for j in range(1, len(inter)):
        yref.append(inter[j])

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

    #AMCL
    estimado=move(myrobot,1,TRst,TRsx,TRsy)
    print("estimado: ", estimado.x, " , ", estimado.y, ' , ', estimado.orientation)
    print("real    : ", TRsx, ' , ', TRsy, ' , ', TRst, '\n')
    distpose = math.dist((estimado.x, estimado.y), (TRsx, TRsy))
    VB_x = (estimado.x - TRsx)/distpose
    VB_y = (estimado.y - TRsy)/distpose
    distangle = math.atan2(VB_y, VB_x)
    resang = diffAngle(distangle, TRst)
    if(distpose < 0.5) and (resang < 0.1):
        TRsx = estimado.x
        TRsy = estimado.y
        TRst = estimado.orientation

    velMsg.linear.x, velMsg.angular.z = Nmpc(
            Xrefp, Yrefp, TRsx, TRsy, TRst, TRsv, TRsw, Xref, Yref, PHIref, Vref, Wref, VXrefp, VYrefp, L1, L2, L3)
    

    print("Querendo ir para X =" ,Xrefp ,", Y =" ,Yrefp)
    print("iRobot.x =" ,TRsx ,", iRobot.y =" ,TRsy)
    print("velo.linear.x =" ,velMsg.linear.x ,", velo.angular.z =" ,velMsg.angular.z)
    
    velPub.publish(velMsg)

    rate.sleep()
    
    
    print("\n\n")
    
print("done")
plt.show()

velMsg.linear.x = 0
velMsg.angular.z = 0
velPub.publish(velMsg)