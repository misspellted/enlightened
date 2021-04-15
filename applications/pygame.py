

from applications import GraphicalApplication
from camera.pygame import PyGameCamera
from camera.viewer import CameraViewer
from cursors.pygame import PyGameCursor
from events import EventHandler
from events.pygame import PyGameEventHandler
from pygame import init, quit, BLEND_RGB_ADD
from pygame.display import set_mode as createWindow, set_caption as captionWindow, flip as refreshWindow
from pygame.event import get as events
from timers.pygame import PyGameMilliseconds


class PyGameApplication(GraphicalApplication, PyGameEventHandler, CameraViewer):
  def __init__(self, length, height, frameRate=60, timer=None, mouseVisible=True):
    GraphicalApplication.__init__(self, length, height)
    init()
    self.timer = PyGameMilliseconds() if timer is None else timer
    self.camera = PyGameCamera(self.timer, frameRate=60)
    self.setCursor(PyGameCursor(self.camera.overlay, mouseVisible=mouseVisible))
    self.camera.attach(self)
    # For now, we'll just configure the sensor to be the same dimensions as the viewer.
    self.camera.configureSensor(*self.dimensions.tupled())
    self.entities = list()
    self.entities.append(self.camera) # TODO: Move the camera ...
    self.cursor = None
    self.baseCaption = None
    self.captionSuffix = None
    self.environment = None # TODO: ... into the environment.

  def setEnvironment(self, environment):
    self.environment = environment

    if self.environment and self.camera:
      self.environment.addEntity(self.camera)

  def createWindow(self):
    return createWindow(self.dimensions.tupled())

  def captionWindow(self, caption):
    captionWindow(caption)

  def setCursor(self, cursor):
    self.cursor = cursor

  def onMousePositionChanged(self, position):
    processed = False

    if self.cursor:
      self.cursor.moveTo(position)
      processed = True

    return processed

  def getEvents(self):
    return events()

  def onQuit(self):
    self.stop()
    return True

  def handle(self, event):
    handled = PyGameEventHandler.handle(self, event)

    # Give the environment a chance to handle the event.
    if not handled and isinstance(self.environment, EventHandler):
      handled = self.environment.handle(event)
    # Should it always get a chance to handle the event?

    if not handled:
      EventHandler.handle(self, event)

    return handled

  def displayFrame(self, frame):
    # TODO: Figure out a better strategy to display the frame.
    #  -- if smaller, do we black-box it, scale up, ?
    #  -- if larger, do we crop it, scale down, ?
    # But if it's identical in size, which is assumed for now,
    # we'll just yeet it into the window.
    self.window.blit(frame, (0, 0))

  def displayOverlay(self, overlay):
    # For now, we assume the overlay is the exact same size.
    self.window.blit(overlay, (0, 0), special_flags=BLEND_RGB_ADD)

  def refreshView(self):
    refreshWindow()

  def update(self):
    deltaTime = self.timer.update()

    if self.cursor:
      self.cursor.update(deltaTime=deltaTime)

    # Only retain entities that remain alive, so as to not waste processing cycles.
    self.entities = [entity for entity in self.entities if entity.alive()]

    # Send an update with delta time to all entities in the environment.
    for entity in self.entities:
      entity.update(deltaTime=deltaTime)

    if self.environment:
      # Chuck in the cursor, so the environment knows where it is, since this class handles the MOUSEMOTION event.
      if self.cursor:
        self.environment.update(deltaTime=deltaTime, cursor=self.cursor)
      else:
        self.environment.update(deltaTime=deltaTime)

      if self.camera:
        self.camera.capture(self.environment)

  def run(self):
    GraphicalApplication.run(self)

  def terminate(self):
    del self.camera
    GraphicalApplication.terminate(self)
    quit()

