

from geometry.vertices import Vertex


class Moving:
  def __init__(self, velocity):
    if not isinstance(velocity, Vertex):
      raise TypeError("Expected 'velocity' to be an instance of Vertex!")
    self.velocity = velocity

