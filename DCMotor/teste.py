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
print("Transfer Function" , transfer_function)

# Step Response
t, y = step_response(transfer_function)
#plotGraph(t, y, 'TF_Step_Response', 'b--')

#PID
pid = PID(50, 0, 0, setpoint=1)
pid.sample_time = 0.01  # Update every 0.01 seconds


sys = feedback(transfer_function, pid, -1)
t2, y2 = step_response(sys)

#k, x = step_response(transfer_function)
plotGraph(t2, y2, 'Controller', 'b--')




