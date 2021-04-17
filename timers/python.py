

from measurements import Measurement
from time import time_ns
from timers import Timer
from units.time import Seconds
from units.prefixes.small import Nano


class PythonTimer(Timer):
  def __init__(self):
    Timer.__init__(self)

  def time(self):
    measurement = Measurement(1, Seconds()).convertTo(Nano())
    measurement.magnitude = time_ns() # Update the magnitude.
    return measurement

