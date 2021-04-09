

from scenes import Scene
from pygame import Surface


class PyGameScene(Scene):
  def __init__(self, timer, length, height):
    Scene.__init__(self, timer, length, height)
    self.scene = Surface(self.dimensions.tupled())

  def render(self):
    return self.scene.copy()

