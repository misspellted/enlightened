

from units.prefixes import Prefix


class Milli(Prefix):
  def __init__(self):
    Prefix.__init__(self, "m", "milli", 1e-3)


class Micro(Prefix):
  def __init__(self):
    Prefix.__init__(self, "μ", "micro", 1e-6)


class Nano(Prefix):
  def __init__(self):
    Prefix.__init__(self, "ns", "nano", 1e-9)

