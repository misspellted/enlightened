

from camera.overlay import CameraOverlay
from pygame import Surface


class PyGameCameraOverlay(CameraOverlay):
  def __init__(self, viewer):
    CameraOverlay.__init__(self, viewer)
    self.overlay = Surface(self.dimensions.tupled()).convert_alpha()

  def captureOverlay(self):
    # Copy the overlay.
    overlay = self.overlay.copy()

    # Reset the overlay for the next capture.
    self.overlay.fill((0, 0, 0))

    return overlay

  def displayRendering(self, rendering, position):
    self.overlay.blit(rendering, position.tupled())

