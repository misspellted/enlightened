

from camera.viewer import CameraViewer
from pygame import BLEND_RGB_ADD
from pygame.display import set_mode, flip

class PyGameCameraViewer(CameraViewer):
  def __init__(self, length, height, frameRate=60):
    CameraViewer.__init__(self, length, height, frameRate)
    self.viewer = set_mode(self.dimensions.tupled())

  def displayFrame(self, frame):
    # TODO: Figure out a better strategy to display the frame.
    #  -- if smaller, do we black-box it, scale up, ?
    #  -- if larger, do we crop it, scale down, ?
    # But if it's identical in size, which is assumed for now,
    # we'll just yeet it into the viewer.
    self.viewer.blit(frame, (0, 0))

  def displayOverlay(self, overlay):
    # For now, we assume the overlay is the exact same size.
    self.viewer.blit(overlay, (0, 0), special_flags=BLEND_RGB_ADD)

  def refreshView(self):
    # print("PyGameCameraViewer::refreshView")
    flip()

