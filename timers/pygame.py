

from pygame.time import get_ticks
from timers import Timer


class PyGameMilliseconds(Timer):
  def __init__(self):
    Timer.__init__(self)

  def sTime(self):
    return get_ticks() / 1000

