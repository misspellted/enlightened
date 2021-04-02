

from scenes import Scene
from pygame import Surface


class PyGameScene(Scene):
  def __init__(self, length, height):
    Scene.__init__(self, length, height)
    self.scene = Surface(self.dimensions.tupled())

  def render(self):
    return self.scene.copy()

