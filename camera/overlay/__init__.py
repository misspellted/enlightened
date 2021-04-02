

from attributes.dimensioned import Dimensioned
from attributes.updated import Updated


class CameraOverlay(Updated, Dimensioned):
  def __init__(self, viewer):
    Dimensioned.__init__(self, viewer.dimensions)
    self.camera = None

  def onAttachment(self, camera):
    self.camera = camera

  def captureOverlay(self):
    raise NotImplementedError()

  def displayRendering(self, rendering, position):
    raise NotImplementedError()

  def update(self):
    # print("CameraOverlay::update")
    # Always capture an overlay.
    self.camera.onOverlayGenerated(self.captureOverlay())

