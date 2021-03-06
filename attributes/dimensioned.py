

from geometry.vertices import Vertex


class Dimensioned:
  def __init__(self, dimensions):
    if not isinstance(dimensions, Vertex):
      raise TypeError("Expected 'dimensions' to be an instance of Vertex!")

    self.dimensions = dimensions

