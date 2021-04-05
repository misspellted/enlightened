

from time import time


class CameraTimer:
  def getTime(self):
    return time() # By default, use Python's standard time library.

  def calculateFrameTime(self, frameRate):
    return 0 if frameRate <= 0 else (1 / frameRate) # Python's standard library uses seonds.

