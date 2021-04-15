

from events import EventHandler
from geometry.vertices import Vertex2
from pygame import QUIT, MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP


class PyGameEventHandler(EventHandler):
  def onQuit(self):
    return False

  def onMousePositionChanged(self, position):
    return False

  def onMouseButtonPressed(self, button):
    return False

  def onMouseButtonReleased(self, button):
    return False

  def handle(self, event):
    handled = False

    if event.type == QUIT:
      handled = self.onQuit()
    elif event.type == MOUSEMOTION:
      handled = self.onMousePositionChanged(Vertex2(*event.pos))
    elif event.type == MOUSEBUTTONDOWN:
      handled = self.onMouseButtonPressed(event.button)
    elif event.type == MOUSEBUTTONUP:
      handled = self.onMouseButtonReleased(event.button)

    return handled

