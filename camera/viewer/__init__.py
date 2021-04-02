

from attributes.dimensioned import Dimensioned
from attributes.updated import Updated
from geometry.vertices import Vertex2
from time import time


class CameraViewer(Updated, Dimensioned):
  def __init__(self, length, height, frameRate=60):
    if length * height <= 0:
      raise ValueError(f"The dimensions of the camera viewer are invalid: [{length}, {height}]")

    Dimensioned.__init__(self, Vertex2(length, height))
    self.targetFrameRate = frameRate
    self.msTargetFrameTime = 0 if frameRate <= 0 else (1 / frameRate)
    self.msAccumulatedTime = 0
    self.lastTime = time()

  def onAttachment(self, camera):
    pass # Do nothing... for now.
    # TODO: Is this where we can possibly determine what kind of
    #   handling to do for different sensor|viewer dimensions?

  def displayFrame(self, frame):
    raise NotImplementedError()

  def displayOverlay(self, overlay):
    raise NotImplementedError()

  def refreshView(self):
    raise NotImplementedError()

  def update(self):
    # print("CameraViewer::update")
    now = time()

    self.msAccumulatedTime += (now - self.lastTime)
    self.lastTime = now

    if self.msTargetFrameTime <= self.msAccumulatedTime:
      if self.msTargetFrameTime == 0:
        self.msAccumulatedTime = 0
      else:
        self.msAccumulatedTime -= self.msTargetFrameTime

      # Refresh the view.
      self.refreshView()

