

from attributes.intervaled import Intervaled
from camera.overlay import CameraOverlay
from camera.sensor import CameraSensor
from camera.viewer import CameraViewer
from entities import Entity
from units.prefixes.small import Milli


DEFAULT_FRAME_RATE = 60


class Camera(Entity, Intervaled):
  def __init__(self, timer, frameRate=DEFAULT_FRAME_RATE):
    resolution = Milli()
    Intervaled.__init__(self, 1 / (resolution.scalor * frameRate), resolution)
    self.viewer = None
    self.overlay = None
    self.sensor = None

  def alive(self):
    return True # The camera, for now, will always be living.

  def die(self):
    pass # And as part of an immortal existence, the request to die is simply ignored.

  def configureOverlay(self, viewer):
    pass

  def configureSensor(self, length, height, frameRate=60):
    pass

  def onFrameCaptured(self, frame):
    if self.viewer:
      self.viewer.displayFrame(frame)

  def attach(self, component):
    if isinstance(component, CameraViewer):
      self.viewer = component
      self.configureOverlay(self.viewer)
    elif isinstance(component, CameraOverlay):
      self.overlay = component
      self.overlay.onAttachment(self)
    elif isinstance(component, CameraSensor):
      self.sensor = component
      self.sensor.onInterval = lambda: self.onFrameCaptured(self.sensor.captureFrame())

  def onOverlayGenerated(self, overlay):
    if self.viewer:
      self.viewer.displayOverlay(overlay)

  def capture(self, environment):
    pass

  def onInterval(self):
    if self.viewer:
      self.viewer.refreshView()

  def update(self, **kwargs):
    deltaTime = kwargs["deltaTime"] if "deltaTime" in kwargs else 0

    if self.sensor:
      self.sensor.update(deltaTime=deltaTime)

    if self.overlay:
      self.overlay.update(deltaTime=deltaTime)

    Intervaled.update(self, **kwargs)

