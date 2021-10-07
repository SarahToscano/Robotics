class PIDControlBlock:
  def __init__(self, Kp, Ki, Kd):
    self.Kp = Kp
    self.Ki = Ki
    self.Kd = Kd
    self.Epr = 0
    self.Eppr = 0
    self.Epppr = 0
    self.Sum = 0
 
  def __call__(self, E): 
    self.Sum += 0.5 * self.Ki * (E + self.Epr)      # where T ~1
    U = self.Kp * E + self.Sum + 0.1667 * self.Kd * (E - self.Epppr + 3.0 * (self.Epr - self.Eppr))
    self.Epppr = self.Eppr
    self.Eppr = self.Epr
    self.Epr = E
    return U