

from attributes.updated import Updated
from camera.overlay import CameraOverlay
from camera.sensor import CameraSensor
from camera.viewer import CameraViewer

class Camera(Updated):
  def __init__(self):
    self.viewer = None
    self.overlay = None
    self.sensor = None

  def configureViewer(self, length, height, frameRate=60):
    raise NotImplementedError()

  def configureOverlay(self, viewer):
    raise NotImplementedError()

  def configureSensor(self, length, height, frameRate=60):
    raise NotImplementedError()

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
    # print("Camera::update")
    if self.sensor:
      self.sensor.update()

    if self.overlay:
      self.overlay.update()

    if self.viewer:
      self.viewer.update()

