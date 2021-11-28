 #! /usr/bin/env python

import math

def laser(msg, teta, x_, y_):
    landmark = []
    for i in range(0, len(msg) -1 , 1):
        d = msg[i]
        if(d != float('inf')):
            if(i >= 0 and i < 180):
                ang = 180 - math.radians(teta - 1.57) - i/2
                x = d*math.sin(ang) + x_
                y = d*math.cos(ang) - y_
            elif(i >= 180 and i < 360):
                ang = math.radians(teta - 1.57) + i/2 - 180
                x = d*math.cos(ang) + x_
                y = d*math.sin(ang) + y_
            elif(i >= 360 and i < 540):
                ang = math.radians(teta - 1.57) + i/2 - 180
                x = d*math.sin(ang) - x_
                y = d*math.cos(ang) + y_
            else:
                ang = math.radians(teta - 1.57) + i/2 - 270
                x = d*math.cos(ang) - x_
                y = d*math.sin(ang) - y_

            landmark.append([x,y])
    return landmark
    


