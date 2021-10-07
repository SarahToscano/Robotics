from pidController import PIDControlBlock
from plant import DcMotor
from feedback import ClosedLoopSystem

if __name__ == "__main__":
  Plant = DcMotor(250, 100)     
  Pid = PIDControlBlock(50, 0, 0)
  Ctrl = ClosedLoopSystem(Pid, Plant)
 
  for i in range(1, 1001):
    print str(Ctrl(100))