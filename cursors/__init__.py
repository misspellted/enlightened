

from attributes.positioned import Positioned
from attributes.updated import Updated


class Cursor(Positioned, Updated):
  def __init__(self, position):
    Positioned.__init__(self, position)

  def moveTo(self, position):
    self.position = position.copy()

