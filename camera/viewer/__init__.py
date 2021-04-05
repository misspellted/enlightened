

from attributes.dimensioned import Dimensioned
from attributes.updated import Updated
from geometry.vertices import Vertex2


class CameraViewer(Updated, Dimensioned):
  def __init__(self, length, height, frameRate=60):
    if length * height <= 0:
      raise ValueError(f"The dimensions of the camera viewer are invalid: [{length}, {height}]")

    Dimensioned.__init__(self, Vertex2(length, height))
    self.targetFrameRate = frameRate
    self.msTargetFrameTime = 0 if frameRate <= 0 else (1 / frameRate)
    self.msAccumulatedTime = 0

  def onAttachment(self, camera):
    pass # Do nothing... for now.
    # TODO: Is this where we can possibly determine what kind of
    #   handling to do for different sensor|viewer dimensions?

  def displayFrame(self, frame):
    pass

  def displayOverlay(self, overlay):
    pass

  def refreshView(self):
    pass

  def update(self, **kwargs):
    deltaTime = kwargs["deltaTime"] if "deltaTime" in kwargs else 0

    self.msAccumulatedTime += deltaTime

    if self.msTargetFrameTime <= self.msAccumulatedTime:
      if self.msTargetFrameTime == 0:
        self.msAccumulatedTime = 0
      else:
        self.msAccumulatedTime -= self.msTargetFrameTime

      # Refresh the view.
      self.refreshView()

