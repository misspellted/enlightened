

from attributes.dimensioned import Dimensioned
from environments import Environment
from geometry.vertices import Vertex2


class PlanarEnvironment(Dimensioned, Environment):
  def __init__(self, timer, dimensions):
    Dimensioned.__init__(self, Vertex2(*dimensions))
    Environment.__init__(self, timer)

