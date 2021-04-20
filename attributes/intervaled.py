

from attributes.updated import Updated
from units.prefixes import Prefix


class Intervaled:
  def __init__(self, interval, resolution):
    if not isinstance(resolution, Prefix):
      raise TypeError("Expected 'resolution' to be an instance of Prefix!")

    self.interval = interval
    self.resolution = resolution

    self.accumulatedTime = 0

  def onInterval(self):
    pass

  def update(self, **kwargs):
    deltaTime = kwargs["deltaTime"] if "deltaTime" in kwargs else None

    if deltaTime:
      self.accumulatedTime += deltaTime.convertTo(self.resolution).magnitude

      if self.interval <= self.accumulatedTime:
        if self.interval == 0:
          self.accumulatedTime = 0
        else:
          while self.interval <= self.accumulatedTime:
            self.accumulatedTime -= self.interval

        self.onInterval()

