

from geometry.vertices import Vertex


class Positioned:
  def __init__(self, position):
    if not isinstance(position, Vertex):
      raise TypeError("Expected 'position' to be an instance of Vertex!")
    self.position = position

  def projectBy(self, delta):
    if not isinstance(delta, Vertex):
      raise TypeError("Expected 'delta' to be an instance of Vertex!")
    return self.position + delta

  def scaleBy(self, scalor):
    self.position *= scalor

  def rotateBy(self, rotation):
    # TODO: Support rotation.
    #       Should an axis be provided?
    pass

