

from geometry.vertices import Vertex


class Accelerated:
  def __init__(self, velocity):
    if not isinstance(velocity, Vertex):
      raise TypeError("Expected 'velocity' to be an instance of Vertex!")
    self.velocity = velocity

  def accelerate(self, acceleration):
    if not isinstance(acceleration, Vertex):
      raise TypeError("Expected 'acceleration' to be an instance of Vertex!")
    self.velocity += acceleration

