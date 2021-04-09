

from camera import Camera, DEFAULT_FRAME_RATE
from camera.sensor.pygame import PyGameCameraSensor
from camera.overlay.pygame import PyGameCameraOverlay
from camera.viewer.pygame import PyGameCameraViewer
import pygame


class PyGameCamera(Camera):
  def __init__(self, environmentTimer, frameRate=DEFAULT_FRAME_RATE):
    Camera.__init__(self, environmentTimer, frameRate)
    pygame.init()

  def configureOverlay(self, viewer):
    self.attach(PyGameCameraOverlay(viewer))

  def configureViewer(self, length, height, frameRate=60):
    self.attach(PyGameCameraViewer(length, height, frameRate))

  def configureSensor(self, length, height, frameRate=60):
    self.attach(PyGameCameraSensor(length, height, frameRate))

  def __del__(self):
    pygame.quit()

