# -*- coding: utf-8 -*-

import math
from diffAngle import *
import numpy as np

PI = math.pi


def costFunction(SimRobx, SimRoby, SimRobteta, SimRobv, SimRobw, Ut, SimTargetx, SimTargety ,SimTargetvx, SimTargetvy , N1, Np, Nu, L1, L2, L3):
    
    sum_cost = 0

    #Others
    sim_time_step = 0.04
    bfc = 1
    dval = 0
    print("\nCOSTFUNCION")
    print("Ut antes do laco = ", Ut)

    for i in range(N1, Np+1):  # Executa 10 vezes
        # corrigindo problemas com angulos
        if i <= Nu:
            v = Ut[0, i-1]
            w = Ut[1, i-1]
        else:
            v = Ut[0, Nu-1]
            w = Ut[1, Nu-1]

        for j in range(0, 4):
            cteta = math.cos(SimRobteta) #VERIFICAR NOVAMENTE SE ESTA EM RAD
            steta = math.sin(SimRobteta)
            print("cteta e steta = ", cteta, " ", steta)

            if SimRobteta > PI:
                SimRobteta = SimRobteta - 2*PI

            SimRobteta = SimRobteta + w*sim_time_step
            print("simrobteta = ", SimRobteta)
            SimRobx = SimRobx + sim_time_step*(v*cteta)
            SimRoby = SimRoby + sim_time_step*(v*steta)
            print("simrob x e y = ", SimRobx, " ", SimRoby)
            SimTargetx = SimTargetx + sim_time_step*SimTargetvx
            SimTargety = SimTargety + sim_time_step*SimTargetvy
            print("simtarget x e y = ", SimTargetx, " ", SimTargety)
            SimTargetvx = SimTargetvx * bfc
            SimTargetvy = SimTargetvy * bfc
            print("simtarget vx e vy = ", SimTargetvx, " ", SimTargetvy)

        RobotTargetDist = math.sqrt(pow((SimTargetx - SimRobx),2) + pow((SimTargety - SimRoby),2))
        print("RobotTargetDist = ", RobotTargetDist)

        RBx = (SimTargetx - SimRobx) / RobotTargetDist
        RBy = (SimTargety - SimRoby) / RobotTargetDist
        print("RB x e y = ", RBx, " ", RBy)

        RobotTargetAngle = math.atan2(RBy, RBx)
        print("RobotTargetAngle = ", RobotTargetAngle)
        sum_cost = sum_cost + L1*abs(dval - RobotTargetDist)

        sum_cost = sum_cost + L2*abs(diffAngle(RobotTargetAngle, SimRobteta))
        # sum_cost = sum_cost + L2*diffAngle(RobotTargetAngle, SimRobteta)
        print("sum_cost = ", sum_cost)
        pass
    #ALEXANDRE
    deltaU = L3*(abs(SimRobv - Ut[0, 0]) + abs(SimRobw - Ut[1, 0]))
    print("deltaU = ", deltaU)
    J = (sum_cost + deltaU)

    return J
