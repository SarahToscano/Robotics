 #! /usr/bin/env python

import math

def toAngle(n):
  return (n*180)/math.pi

def laser(msg, teta, x_, y_):
    landmark = []
    for i in range(0, len(msg), 33):
        d = msg[i]
        if(d != float('inf')):
            if(teta < 0):
                teta = 6.2831531 + teta
            ang = toAngle(teta - 1.57) + i/2
            if(ang > 360):
                ang = ang - 360
            if(ang < 90):
                x = d*math.sin(math.radians(ang)) + x_
                y = y_ - d*math.cos(math.radians(ang))
            elif(ang >= 90 and ang < 180):
                #print('aqui')
                x = d*math.cos(math.radians(ang-90)) + x_
                #print('d = ', d, ' cos = ', math.cos(math.radians(ang-90)), ' x_ = ',x_)
                y = d*math.sin(math.radians(ang-90)) + y_
            elif(ang >= 180 and ang < 270):
                x = x_ - d*math.sin(math.radians(ang-180)) 
                y = d*math.cos(math.radians(ang-180)) + y_
            else:
                x = x_ - d*math.cos(math.radians(ang -270)) 
                y = y_ - d*math.sin(math.radians(ang-270)) 
       
            landmark.append([x,y])
            #print('teta = ', teta,' i/2 = ', i/2, ' ang = ', ang, ' posicoes = ',[x,y])
    return landmark
    


