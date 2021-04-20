

from attributes.rendered import Rendered
from camera import Camera, DEFAULT_FRAME_RATE
from camera.sensor.pygame import PyGameCameraSensor
from camera.overlay.pygame import PyGameCameraOverlay
from geometry.vertices import Vertex2
import pygame


class PyGameCamera(Camera):
  def __init__(self, timer, frameRate=DEFAULT_FRAME_RATE):
    Camera.__init__(self, timer, frameRate)

  def configureOverlay(self, viewer):
    self.attach(PyGameCameraOverlay(viewer))

  def configureSensor(self, length, height, frameRate=60):
    print(f"Configuring PyGameCamera sensor: {length} x {height} @ {frameRate} frames")
    self.attach(PyGameCameraSensor(length, height, frameRate))

  def capture(self, environment):
    captured = None

    if isinstance(environment, Rendered):
      captured = environment.render()

      if captured and self.sensor:
        self.sensor.displayRendering(captured, Vertex2(0, 0))

