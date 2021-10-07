class ClosedLoopSystem:
  def __init__(self, controller, plant) :
    self.P = plant
    self.C = controller
    self.Ypr = 0
 
  def __call__(self, X):
    E = X - self.Ypr
    U = self.C(E)
    Y = self.P(U)
    self.Ypr = Y
    return Y