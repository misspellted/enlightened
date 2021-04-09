

from time import time, time_ns
from timers import Timer, TimeIntervals


class PythonSeconds(Timer):
  def __init__(self):
    Timer.__init__(self, TimeIntervals.SECOND)

  def getTime(self):
    return time()


class PythonNanoseconds(Timer):
  def __init__(self):
    Timer.__init__(self, TimeIntervals.NANOSECOND)

  def getTime(self):
    return time_ns()

