

from attributes.dimensioned import Dimensioned
from events import EventHandler
from geometry.vertices import Vertex2


# Selected portions borrowed from
# https://github.com/misspellted/viewted/blob/main/application/__init__.py
# (Intent is to either absorb enlighted into viewted, or vice versa.)
class Application(EventHandler):
  def __init__(self):
    self.running = False

  # TODO: Likely the location to put the onKeyPressed/onKeyReleased methods..

  def getEvents(self):
    return list()

  def process(self):
    for event in self.getEvents():
      self.handle(event)

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


class GraphicalApplication(Application, Dimensioned):
  def __init__(self, length, height):
    Application.__init__(self)
    Dimensioned.__init__(self, Vertex2(length, height))
    self.window = self.createWindow()

  def createWindow(self):
    return None

  def captionWindow(self, caption):
    return None

  def terminate(self):
    if self.window:
      del self.window

