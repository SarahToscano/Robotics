# -*- coding: utf-8 -*-

import math

PI = math.pi

#VERifICAR O QuE Foi uSAdONA CadeiRa e ROboTIcA 
def diffAngle(a1, a2):
    ang = int(a1-a2)

    if ang < 0:
        ang = int(-((-ang/(2*PI))-math.floor((-ang/(2*PI)))*2*PI))

    if ang < PI:
        ang = int(ang + (2*PI))
    else:
        #print("ang = ", ang)
        ang = int(((ang/(2 * PI)) - math.floor((ang/(2 * PI)))) * (2 * PI))

    if ang > PI:
        ang = int(ang - (2 * PI))
        
    return ang

