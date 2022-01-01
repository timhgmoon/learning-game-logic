#LEARNING INHERITANCE
class Computation:
  def __init__(self, x, y):
    self.x = x
    self.y = y
  
  def compute(self):
    pass
class Sum(Computation):
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def compute(self):
    return self.x + self.y

class Product(Computation):
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def compute(self):
    return self.x * self.y