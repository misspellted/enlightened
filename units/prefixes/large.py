

from units.prefixes import Prefix


class Kilo(Prefix):
  def __init__(self):
    Prefix.__init__(self, "k", "kilo", 1e3)

