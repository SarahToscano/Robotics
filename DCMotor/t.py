from simple_pid import PID
from plotter import plotGraph
from matplotlib.pyplot import * # Grab MATLAB plotting functions
from control import * # MATLAB-like functions

# Transfer Function
num = [[[0.7522]]]
den = [[[1,0.082]]]
print(num)
print(den)
transfer_function = TransferFunction(num, den)
print(type(transfer_function))
print("Transfer Function" , transfer_function)

# Step Response
t, y = step_response(transfer_function)
print(type(t))
print("Transfer Function" , t)
plotGraph(t, y, 'TF_Step_Response', 'b--')