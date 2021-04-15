

from units import Unit


class Prefix:
  def __init__(self, symbol, prefix, scalor):
    self.symbol = symbol
    self.prefix = prefix
    self.scalor = scalor


class PrefixedUnit(Unit):
  def __init__(self, prefix, unit):
    symbol = f"{prefix.symbol}{unit.symbol}"
    notation = f"{prefix.prefix}{unit.notation}"
    plurality = f"{prefix.prefix}{unit.plurality}"
    Unit.__init__(self, symbol, notation, plurality)
    self.prefix = prefix
    self.unit = unit

