

from measurements import Measurement
from pygame.time import get_ticks
from timers import Timer
from units.time import Seconds
from units.prefixes.small import Milli


class PyGameTimer(Timer):
  def __init__(self):
    Timer.__init__(self)

  def time(self):
    measurement = Measurement(1, Seconds()).convertTo(Milli())
    measurement.magnitude = get_ticks() # Update the magnitude.
    return measurement

