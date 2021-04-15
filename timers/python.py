

from time import time, time_ns
from timers import Timer


class PythonSeconds(Timer):
  def __init__(self):
    Timer.__init__(self)

  def sTime(self):
    return time()


class PythonNanoseconds(Timer):
  def __init__(self):
    Timer.__init__(self)

  def sTime(self):
    return time_ns() / 1e-9

