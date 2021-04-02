

from attributes.positioned import Positioned
from attributes.accelerated import Accelerated
from geometry.vertices import Vertex2


class Moving2(Positioned, Accelerated):
  def __init__(self, position, velocity):
    Positioned.__init__(self, Vertex2(*position))
    Accelerated.__init__(self, Vertex2(*velocity))

