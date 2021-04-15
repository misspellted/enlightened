

from camera.overlay import CameraOverlay
from camera.sensor import CameraSensor
from camera.viewer import CameraViewer
from entities import Entity


DEFAULT_FRAME_RATE = 60


class Camera(Entity):
  def __init__(self, timer, frameRate=DEFAULT_FRAME_RATE):
    self.targetFrameRate = frameRate
    self.targetFrameTime = 0 if frameRate <= 0 else (1000 / frameRate) # Targeting ms resolution.
    self.accumulatedTime = 0
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

  def attach(self, component):
    if isinstance(component, CameraViewer):
      self.viewer = component
      self.configureOverlay(self.viewer)
    elif isinstance(component, CameraOverlay):
      self.overlay = component
      self.overlay.onAttachment(self)
    elif isinstance(component, CameraSensor):
      self.sensor = component
      self.sensor.onAttachment(self)

  def onFrameCaptured(self, frame):
    if self.viewer:
      self.viewer.displayFrame(frame)

  def onOverlayGenerated(self, overlay):
    if self.viewer:
      self.viewer.displayOverlay(overlay)

  def capture(self, environment):
    pass

  def update(self, **kwargs):
    deltaTime = kwargs["deltaTime"] if "deltaTime" in kwargs else 0

    if self.sensor:
      self.sensor.update(deltaTime=deltaTime)

    if self.overlay:
      self.overlay.update(deltaTime=deltaTime)

    self.accumulatedTime += deltaTime

    if self.targetFrameTime <= self.accumulatedTime:
      if self.targetFrameTime == 0:
        self.accumulatedTime = 0
      else:
        while self.targetFrameTime < self.accumulatedTime:
          self.accumulatedTime -= self.targetFrameTime

      if self.viewer:
        self.viewer.refreshView()

