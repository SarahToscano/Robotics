import numpy as np
from plotter import plotGraph
import math

# DC Motor Parameters# 

#Armature
Ra = 1.5586
La = 0.0001

#Fild
Rf = 0.5
Lf = 0.001
Vf = 1

#Mechanical Parameters #
Jm = 9.356*(10^-6)
Fm = 0.0001
Km = 0.0109

#Frequency Discretization
h = 0.000001

WRef = 125
Tm = 0

#PID Controller #
Kp = -0.2339
Ki = 47.6164
Kd = 0.0012
D = Kd/h
PD = -Kp - 2*Kd/h
PID = Kp + Ki*(h) + Kd/(h)

t=0

#Arrays

Ia = [0]*300000
If= [0]*300000
Wr= [0]*300000
Erro= [0]*300000
Va= [0]*300000
x= [0]*300000
Yt= [0]*300000

while (t<=300000-1):
    if (t<=5): 
        Ia[t] = 0
        If[t] = 0
        Wr[t] = 0
        Erro[t] = WRef
        Va[t] = 0
        Yt[t] = 0

    else:
        Erro[t] = WRef - Wr[t-1]
        Va[t] = (Erro[t] *(PID) + Erro[t-1]*PD + Erro[t-2]*D) + Va[t-1]

        If[t] = If[t-1] + (((-Rf/Lf)*If[t-1] + Vf/Lf)*h)
        
        Ia[t] = Ia[t-1] + (((-Ra/La)*Ia[t-1] + Va[t-1]/Lf - (Km/La)*If[t-1]*Wr[t-1]) *h)
        
        Wr[t] = Wr[t-1] + (((-Fm/Jm)*Wr[t-1] + (Km/Jm)*If[t-1]*Ia[t-1] - Tm/Jm) *h)
    
        Yt[t] = Yt[t-1] + ((0.7522*(1- math.exp(-t/(1/0.0082))))*0.000001)
    t+=1

#Define o array que representa o eixo X       
for i in range (0, 300000, 1):
    x[i]=i/0.000001


#plotGraph(x, Ia, 'Ia')
plotGraph(x, Yt, 'Wr')

    