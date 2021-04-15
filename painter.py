

from applications.pygame import PyGameApplication
from cursors.pygame import PyGameCursor
from defaults import DEMO_WINDOW_LENGTH, DEMO_WINDOW_HEIGHT
import pygame
from scenes.pygame import PyGameScene


class PaintingScene(PyGameScene):
  def __init__(self, timer, length, height):
    PyGameScene.__init__(self, timer, length, height)
    self.painting = False
    self.paintColor = (127, 0, 0)
    self.erasing = False
    self.eraseColor = (0, 0, 0)

  def onMouseButtonPressed(self, button):
    handled = False

    if button == pygame.BUTTON_LEFT:
      self.painting = True
      handled = True
    elif button == pygame.BUTTON_RIGHT:
      self.erasing = True
      handled = True

    return handled

  def onMouseButtonReleased(self, button):
    handled = False

    if button == pygame.BUTTON_LEFT:
      self.painting = False
      handled = True
    elif button == pygame.BUTTON_RIGHT:
      self.erasing = False
      handled = True

    return handled

  def update(self, **kwargs):
    cursor = kwargs["cursor"] if "cursor" in kwargs else None

    if cursor:
      # Draw a circle any time we're "painting" or "erasing".
      if self.painting:
        pygame.draw.circle(self.scene, self.paintColor, cursor.position.tupled(), cursor.radius, 1)
      elif self.erasing:
        pygame.draw.circle(self.scene, self.eraseColor, cursor.position.tupled(), cursor.radius, 1)


class PainterDemo(PyGameApplication):
  def __init__(self, length, height, mouseVisible=True):
    PyGameApplication.__init__(self, length, height, mouseVisible=mouseVisible)
    self.setCursor(PyGameCursor(self.camera.overlay, mouseVisible=mouseVisible))
    self.setEnvironment(PaintingScene(self.timer, length, height))
    self.captionWindow("Painter Demo")


if __name__ == "__main__":
  demo = PainterDemo(DEMO_WINDOW_LENGTH, DEMO_WINDOW_HEIGHT, False)
  demo.run()
  del demo

