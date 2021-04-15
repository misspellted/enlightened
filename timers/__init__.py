

from attributes.updated import Updated


class Timer(Updated):
  def __init__(self):
    self.lastTime = self.sTime()

  def sTime(self):
    raise NotImplementedError()

  def update(self, **kwargs):
    now = self.sTime()
    deltaTime = now - self.lastTime
    self.lastTime = now
    return deltaTime

