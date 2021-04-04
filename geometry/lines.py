

from geometry.vertices import Vertex


class Segment:
  def __init__(self, debut, arret):
    if not isinstance(debut, Vertex):
      raise TypeError("Expected 'debut' to be an instance of Vertex!")
    if not isinstance(arret, Vertex):
      raise TypeError("Expected 'arret' to be an instance of Vertex!")
    self.debut = debut
    self.arret = arret

  @property
  def directional(self):
    return self.arret - self.debut


# class Line:
#   """
#   A line, defined in terms of a starting position, and a directional vector.

#   Based on https://math.stackexchange.com/a/799859.
#   """
#   def __init__(self, debut, directional):
#     self.debut = debut
#     self.directional = directional

#   def at(self, t):
#     # Applies the directional 't' times.
#     current = self.debut.copy()
#     for _ in range(t):
#       current += self.directional
#     return current

