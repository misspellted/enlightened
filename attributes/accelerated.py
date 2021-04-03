

from geometry.vertices import Vertex


class Accelerated:
  def __init__(self, acceleration):
    if not isinstance(acceleration, Vertex):
      raise TypeError("Expected 'acceleration' to be an instance of Vertex!")
    self.acceleration = acceleration

