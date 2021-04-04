

from attributes.dimensioned import Dimensioned
from attributes.rendered import Rendered
from geometry.vertices import Vertex2


class Scene(Dimensioned, Rendered):
  def __init__(self, length, height):
    if length * height <= 0:
      raise ValueError(f"The dimensions of the scene are invalid: [{length}, {height}]")

    Dimensioned.__init__(self, Vertex2(length, height))

