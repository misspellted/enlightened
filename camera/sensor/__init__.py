

from attributes.dimensioned import Dimensioned
from attributes.intervaled import Intervaled
from geometry.vertices import Vertex2
from units.prefixes.small import Milli


DEFAULT_FRAME_RATE = 60


class CameraSensor(Dimensioned, Intervaled):
  def __init__(self, length, height, frameRate=DEFAULT_FRAME_RATE):
    if length * height <= 0:
      raise ValueError(f"The dimensions of the camera sensor are invalid: [{length}, {height}]")

    Dimensioned.__init__(self, Vertex2(length, height))
    resolution = Milli()
    Intervaled.__init__(self, 1 / (resolution.scalor * frameRate), resolution)

  def sense(self, thing):
    pass # Not sure if this is the best name for the method/function/thing.. d^_^b

  def captureFrame(self):
    pass

  def displayRendering(self, rendering, position):
    pass

