

from geometry.lines import Segment
from attributes.living import Living
from attributes.moving import Moving2
from entities import Entity
from random import random
from utilities import reflect
from pygame.draw import line as aline, aaline


MAXIMUM_TRAIL_LENGTH = 500


class Ray(Living, Moving2, Entity):
  def __init__(self, life, position, rayColor, trailLength=MAXIMUM_TRAIL_LENGTH):
    Moving2.__init__(self, position, (random() - 0.5, random() - 0.5))
    self.life = 0 if life < 0 else life
    self.rayColor = rayColor
    self.trail = list()
    self.trailLength = trailLength if 0 <= trailLength <= MAXIMUM_TRAIL_LENGTH else MAXIMUM_TRAIL_LENGTH

  def alive(self):
    return 0 < self.life

  def bounce(self):
    pass # Do nothing on the notification that a bounce occurred.

  def live(self, **kwargs):
    space = kwargs["space"] if "space" in kwargs else None

    if space:
      lastPosition = self.position
      # print(f"[{self.velocity.x, self.velocity.y}] @ ({self.position.x}, {self.position.y})")

      # Project the ray's future position.
      # projected = self.projectBy(self.velocity)

      # TODO: Check the boundaries here.

      # Reflect the ray if necessary.
      self.position.x, self.velocity.x = reflect(0, self.position.x, self.velocity.x, space[0])
      self.position.y, self.velocity.y = reflect(0, self.position.y, self.velocity.y, space[1])

      # print(f"[{self.velocity.x, self.velocity.y}] @ ({self.position.x}, {self.position.y})")

      while self.trailLength < len(self.trail):
        self.trail.pop(0)

      self.trail.append(Segment(lastPosition, self.position))

      self.life -= 1

  def update(self, **kwargs):
    if self.alive():
      self.live(**kwargs)

    return self.alive()

  def draw(self, surface):
    # for segment in self.trail:
    segment = self.trail[-1]
    debut = segment.debut.tupled()
    arret = segment.arret.tupled()
    try:
      aline(surface, self.rayColor, debut, arret)
      # aaline(surface, self.rayColor, debut, arret)
    except TypeError as oops:
      print(f"Failed at {debut} -> {arret}: {oops}!")

