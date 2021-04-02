

class Rectangle:
  def __init__(self, length, height):
    self.length = length
    self.height = height


class CenteredRectangle(Rectangle):
  def __init__(self, center, length, height):
    Rectangle.__init__(self, length, height)
    self.center = center

