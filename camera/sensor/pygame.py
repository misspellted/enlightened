

from attributes.dimensioned import Dimensioned
from attributes.positioned import Positioned
from camera.sensor import CameraSensor
from pygame import Surface


class PyGameCameraSensor(CameraSensor):
  def __init__(self, length, height, frameRate=60):
    CameraSensor.__init__(self, length, height, frameRate)
    self.sensor = Surface(self.dimensions.tupled())

  def captureFrame(self):
    # Copy the sensor data as a frame.
    frame = self.sensor.copy()

    # Reset the sensor for the next frame.
    self.sensor.fill((0, 0, 0))

    return frame

  def displayRendering(self, rendering, position):
    self.sensor.blit(rendering, position.tupled())

