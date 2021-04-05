

from attributes.updated import Updated
from camera.overlay import CameraOverlay
from camera.sensor import CameraSensor
from camera.timers import CameraTimer
from camera.viewer import CameraViewer


DEFAULT_FRAME_RATE = 60


class Camera(Updated):
  def __init__(self, frameRate=DEFAULT_FRAME_RATE):
    self.targetFrameRate = frameRate
    self.timer = CameraTimer()
    self.msTargetFrameTime = self.timer.calculateFrameTime(frameRate)
    self.msAccumulatedTime = 0
    self.viewer = None
    self.overlay = None
    self.sensor = None
    self.lastTime = self.timer.getTime()

  def configureViewer(self, length, height, frameRate=60):
    pass

  def configureOverlay(self, viewer):
    pass

  def configureSensor(self, length, height, frameRate=60):
    pass

  def attach(self, component):
    if isinstance(component, CameraViewer):
      self.viewer = component
      self.configureOverlay(self.viewer)
      self.viewer.onAttachment(self)
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

  def update(self):
    now = self.timer.getTime()
    deltaTime = now - self.lastTime
    self.lastTime = now

    if self.sensor:
      self.sensor.update(deltaTime=deltaTime)

    if self.overlay:
      self.overlay.update(deltaTime=deltaTime)

    if self.viewer:
      self.viewer.update(deltaTime=deltaTime)

    self.msAccumulatedTime += deltaTime

    if self.msTargetFrameTime <= self.msAccumulatedTime:
      if self.msTargetFrameTime == 0:
        self.msAccumulatedTime = 0
      else:
        self.msAccumulatedTime -= self.msTargetFrameTime

