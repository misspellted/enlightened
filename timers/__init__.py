

from attributes.updated import Updated
from measurements import Measurement
from time import time
from units.time import Seconds


class Timer(Updated):
  def __init__(self):
    self.lastTime = self.time()

  def time(self):
    return Measurement(time(), Seconds())

  def update(self, **kwargs):
    now = self.time()
    deltaTime = Measurement(now.magnitude - self.lastTime.magnitude, now.unit)
    self.lastTime = now
    return deltaTime

