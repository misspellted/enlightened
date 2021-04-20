

from attributes.dimensioned import Dimensioned
from attributes.rendered import Rendered
from cursors import Cursor
from geometry.vertices import Vertex2
from pygame import Surface
from pygame.draw import circle as drawCircle
from pygame.mouse import set_visible as setMouseVisibility


class PyGameCursor(Cursor, Dimensioned, Rendered):
  def __init__(self, cameraOverlay, radius=20, mouseVisible=True):
    self.cameraOverlay = cameraOverlay
    Cursor.__init__(self, Vertex2(0, 0))
    Dimensioned.__init__(self, Vertex2(radius * 2, radius * 2))
    self.radius = radius
    self.color = (191, 191, 191)
    setMouseVisibility(mouseVisible)

  def render(self):
    rendering = Surface(self.dimensions.tupled()).convert_alpha()
    drawCircle(rendering, self.color, (self.radius, self.radius), self.radius, 1)
    return rendering

  def update(self, **kwargs):
    # Render unto the overlay thine .. rendering..?
    self.cameraOverlay.displayRendering(self.render(), self.position - Vertex2(self.radius, self.radius))