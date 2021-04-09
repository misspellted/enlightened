

from attributes.updated import Updated
from demos import PyGameApp, DEMO_WINDOW_LENGTH, DEMO_WINDOW_HEIGHT
from geometry.vertices import Vertex2
import pygame
from scenes.pygame import PyGameScene


class PaintingScene(PyGameScene, Updated):
  def __init__(self, timer, length, height):
    PyGameScene.__init__(self, timer, length, height)
    self.painting = False
    self.paintColor = (127, 0, 0)
    self.erasing = False
    self.eraseColor = (0, 0, 0)

  def onMouseButtonDown(self, event):
    handled = False

    if event.button == pygame.BUTTON_LEFT:
      self.painting = True
      handled = True
    elif event.button == pygame.BUTTON_RIGHT:
      self.erasing = True
      handled = True

    return handled

  def onMouseButtonUp(self, event):
    handled = False

    if event.button == pygame.BUTTON_LEFT:
      self.painting = False
      handled = True
    elif event.button == pygame.BUTTON_RIGHT:
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



class PaintingDemo(PyGameApp):
  def __init__(self):
    PyGameApp.__init__(self)
    self.scene = None
    self.cameraSensor = None

  def onCameraSensorConfigured(self, cameraSensor):
    length, height = cameraSensor.dimensions.tupled()
    self.scene = PaintingScene(self.timer, length, height)
    self.cameraSensor = cameraSensor

  def onMouseButtonDown(self, event):
    return False if not self.scene else self.scene.onMouseButtonDown(event)

  def onMouseButtonUp(self, event):
    return False if not self.scene else self.scene.onMouseButtonUp(event)

  def update(self):
    PyGameApp.update(self)

    rendering = None

    if self.scene:
      self.scene.update(cursor=self.cursor)
      rendering = self.scene.render()

    if self.cameraSensor and rendering:
      self.cameraSensor.displayRendering(rendering, Vertex2(0, 0))


# This demo can be invoked directly, using the following command while in the
#   directory of the repository:
#
#     python -m demos.painter
if __name__ == "__main__":
  demo = PaintingDemo()
  demo.run(DEMO_WINDOW_LENGTH, DEMO_WINDOW_HEIGHT, False)
  del demo

