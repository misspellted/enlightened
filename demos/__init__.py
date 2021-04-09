

from attributes.dimensioned import Dimensioned
from attributes.positioned import Positioned
from attributes.rendered import Rendered
from attributes.updated import Updated
from camera.pygame import PyGameCamera
from geometry.vertices import Vertex2
import pygame
from timers.pygame import PyGameMilliseconds
from timers.python import PythonSeconds, PythonNanoseconds


DEMO_WINDOW_LENGTH = 640
DEMO_WINDOW_HEIGHT = 480
# DEMO_WINDOW_LENGTH = 1280
# DEMO_WINDOW_HEIGHT = 720


# Selected portions borrowed from
# https://github.com/misspellted/viewted/blob/main/application/__init__.py
# (Intent is to either absorb enlighted into viewted, or vice versa.)
class Application:
  def __init__(self):
    self.running = False

  def process(self):
    pass

  def update(self):
    pass

  def terminate(self):
    pass

  def run(self):
    self.running = True

    while self.running:
      self.process()

      if self.running:
        self.update()
      else:
        self.terminate()

  def stop(self):
    self.running = False


class PyGameCursor(Positioned, Rendered, Updated):
  def __init__(self, cameraOverlay, radius=20, cursorVisible=True):
    self.cameraOverlay = cameraOverlay
    Positioned.__init__(self, Vertex2(0, 0))
    Dimensioned.__init__(self, Vertex2(radius * 2, radius * 2))
    self.radius = radius
    self.color = (191, 191, 191)
    pygame.mouse.set_visible(cursorVisible)

  def onCursorPositioned(self, position):
    self.position = Vertex2(*position)# - Vertex2(self.radius, self.radius)
    return True

  def render(self):
    rendering = pygame.Surface(self.dimensions.tupled()).convert_alpha() # ?
    pygame.draw.circle(rendering, self.color, (self.radius, self.radius), self.radius, 1)
    return rendering

  def update(self):
    # Render unto the overlay thine .. rendering..?
    self.cameraOverlay.displayRendering(self.render(), self.position - Vertex2(self.radius, self.radius))


class PyGameApp(Application):
  def __init__(self):
    Application.__init__(self)
    # self.timer = PythonSeconds()
    self.timer = PyGameMilliseconds()
    # self.timer = PythonNanoseconds()
    self.camera = PyGameCamera(self.timer)
    self.cursor = None
    self.updates = 0
    self.baseCaption = None
    self.captionSuffix = None
    self.cursorVisible = False

  def update(self):
    self.updates += 1
    self.camera.update()

    if self.cursor:
      self.cursor.update()

    if self.baseCaption:
      caption = self.baseCaption

      if self.captionSuffix:
        caption += self.captionSuffix

      pygame.display.set_caption(caption)

  def onCameraViewerConfigured(self, cameraViewer):
    pass # Do nothing by default.

  def onCameraOverlayConfigured(self, cameraOverlay):
    self.cursor = PyGameCursor(self.camera.overlay, cursorVisible=self.cursorVisible)

  def onCameraSensorConfigured(self, cameraSensor):
    pass # Do nothing by default.

  def run(self, windowLength, windowHeight, cursorVisible=True):
    # For now, we'll just configure the sensor and the viewer to be the same dimensions.
    self.camera.configureViewer(windowLength, windowHeight) # An overlay is automatically configured.
    self.onCameraViewerConfigured(self.camera.viewer)
    self.onCameraOverlayConfigured(self.camera.overlay)
    self.camera.configureSensor(windowLength, windowHeight)
    self.onCameraSensorConfigured(self.camera.sensor)
    self.cursorVisible = cursorVisible
    Application.run(self)

  def onMouseMotion(self, event):
    self.cursor.onCursorPositioned(event.pos)
    return True

  def onMouseButtonDown(self, event):
    return False

  def onMouseButtonUp(self, event):
    return False

  def process(self):
    """
    Processes the pygame event queue.

    The QUIT event is handled internally by calling the ::stop method, setting
    up the termination sequence.
    
    Any other event (for now) is forwarded to ::handle for further processing.
    """
    for event in pygame.event.get():
      handled = False

      if event.type == pygame.QUIT:
        self.stop()
        handled = True
        break
      elif event.type == pygame.MOUSEMOTION:
        handled = self.onMouseMotion(event)
      elif event.type == pygame.MOUSEBUTTONDOWN:
        handled = self.onMouseButtonDown(event)
      elif event.type == pygame.MOUSEBUTTONUP:
        handled = self.onMouseButtonUp(event)

      if not handled:
        print(event)

  def terminate(self):
    del self.camera
    Application.terminate(self)

