

from pygame.time import get_ticks
from timers import Timer, TimeIntervals


class PyGameMilliseconds(Timer):
  def __init__(self):
    Timer.__init__(self, TimeIntervals.MILLISECOND)

  def getTime(self):
    return get_ticks()

