

from units.prefixes import PrefixedUnit


class Measurement:
  def __init__(self, magnitude, unit):
    self.magnitude = magnitude
    self.unit = unit

  def inBaseUnits(self):
    unit = self.unit
    scalor = 1

    if isinstance(unit, PrefixedUnit):
      scalor = 1 / unit.prefix.scalor
      unit = unit.unit

    return Measurement(self.magnitude / scalor, unit)

  def convertTo(self, prefix):
    baseUnits = self.inBaseUnits()

    return Measurement(baseUnits.magnitude / prefix.scalor, PrefixedUnit(prefix, baseUnits.unit))

  def __str__(self):
    return f"{self.magnitude} {self.unit.notation if self.magnitude == 1 else self.unit.plurality}"

