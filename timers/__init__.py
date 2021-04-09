

from attributes.updated import Updated


class TimeIntervals:
  SECOND = -3
  MILLISECOND = 0       # Target reporting elapsed time in milliseconds.
  MICROSECOND = 3
  NANOSECOND = 6

  RECOGNIZED = [SECOND, MILLISECOND, MICROSECOND, NANOSECOND]


class Timer(Updated):
  def __init__(self, interval=TimeIntervals.MILLISECOND):
    if interval is None:
      raise ValueError("`interval` is required!")
    elif interval not in TimeIntervals.RECOGNIZED:
      raise ValueError(f"`interval` is not recognized: {interval}")

    self.interval = interval
    self.scalor = pow(10, interval)
    self.lastTime = self.getTime()

  def getTime(self):
    raise NotImplementedError()

  def update(self, **kwargs):
    now = self.getTime()
    deltaTime = (now - self.lastTime) / self.scalor
    self.lastTime = now
    return deltaTime


# if __name__ == "__main__":
#   from time import sleep, time, time_ns

#   print(f"1 millisecond == {pow(10, TimeIntervals.SECOND)} second(s)")
#   print(f"1 millisecond == {pow(10, TimeIntervals.MILLISECOND)} millisecond(s)")
#   print(f"1 millisecond == {pow(10, TimeIntervals.MICROSECOND)} microsecond(s)")
#   print(f"1 millisecond == {pow(10, TimeIntervals.NANOSECOND)} nanosecond(s)")

#   sDebut = time()
#   sleep(1)
#   sArret = time()

#   print(f"delta Seconds: {sArret - sDebut} -> {(sArret - sDebut) / pow(10, TimeIntervals.SECOND)} millisecond(s)")

#   nsDebut = time_ns()
#   sleep(1)
#   nsArret = time_ns()

#   print(f"delta Nanoseconds {nsArret - nsDebut} -> {(nsArret - nsDebut) / pow(10, TimeIntervals.NANOSECOND)} millisecond(s)")

