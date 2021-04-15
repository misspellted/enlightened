

from attributes.dimensioned import Dimensioned
from attributes.updated import Updated
from geometry.vertices import Vertex2


class CameraSensor(Updated, Dimensioned):
  def __init__(self, length, height, frameRate=60):
    if length * height <= 0:
      raise ValueError(f"The dimensions of the camera sensor are invalid: [{length}, {height}]")

    Dimensioned.__init__(self, Vertex2(length, height))
    self.targetFrameRate = frameRate
    self.targetFrameTime = 0 if frameRate <= 0 else (1 / frameRate)
    self.accumulatedTime = 0
    self.camera = None

  def onAttachment(self, camera):
    self.camera = camera

  def sense(self, thing):
    pass # Not sure if this is the best name for the method/function/thing.. d^_^b

  def captureFrame(self):
    pass

  def displayRendering(self, rendering, position):
    pass

  def update(self, **kwargs):
    deltaTime = kwargs["deltaTime"] if "deltaTime" in kwargs else 0

    self.accumulatedTime += deltaTime

    if self.targetFrameTime <= self.accumulatedTime:
      if self.targetFrameTime == 0:
        self.accumulatedTime = 0
      else:
        self.accumulatedTime -= self.targetFrameTime

      # Send the captured frame.
      self.camera.onFrameCaptured(self.captureFrame())

