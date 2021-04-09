

from attributes.moving import Moving
from attributes.positioned import Positioned
from entities import Entity
from geometry.lines import Segment
from pygame.draw import line as aline, aaline
from random import random


RAY_BOUNCES = 4
RAY_TRAIL_LENGTH = 500


def reflect(lower, current, modifier, upper):
  next, modified = current, modifier

  if next + modified < lower:
    modified *= -1
    next = lower + (modified - next + lower)
  elif upper < next + modified:
    next = upper - (next + modified - upper)
    modified *= -1
  else:
    next += modified

  return (next, modified)


class Ray(Positioned, Moving, Entity):
  def __init__(self, position, velocity, rayColor=None, trailLength=RAY_TRAIL_LENGTH):
    Positioned.__init__(self, position)
    Moving.__init__(self, velocity)
    
    self.lastPosition = None
    self.rayColor = rayColor if rayColor else (int(random() * 255), int(random() * 255), int(random() * 255))
    self.bounces = RAY_BOUNCES
    self.trail = list()
    self.trailLength = trailLength if 0 <= trailLength <= RAY_TRAIL_LENGTH else MAXIMUM_TRAIL_LENGTH

  def alive(self):
    return 0 < self.bounces

  def onReflection(self):
    self.bounces -= 1

  def live(self, **kwargs):
    environment = kwargs["environment"] if "environment" in kwargs else None

    if environment:
      length, height = environment.dimensions.tupled()
      # Track only the last few positions.
      self.trail = self.trail[:-(self.trailLength - 1)]

      self.lastPosition = self.position
      lastVelocity = self.velocity

      # Reflect the ray if necessary.
      px, vx = reflect(0, self.position.x, self.velocity.x, length)
      py, vy = reflect(0, self.position.y, self.velocity.y, height)

      if self.velocity.x != vx or self.velocity.y != vy:
        self.onReflection()

      # TODO: Use perception (do a perception check! lol) to determine
      # near-by entities that might cause interfere with the projection.

      # Project the ray's future position.
      # projected = self.projectBy(self.velocity)

      self.position.x = px
      self.position.y = py
      self.velocity.x = vx
      self.velocity.y = vy
      
      # Add the latest segement.
      self.trail.append(Segment(self.lastPosition, self.position))

  def update(self, **kwargs):
    if self.alive():
      self.live(**kwargs)

  def die(self):
    self.bounces = 0

  def draw(self, surface):
    for segment in self.trail:
      debut = segment.debut.tupled()
      arret = segment.arret.tupled()
      try:
        aline(surface, self.rayColor, debut, arret)
        # aaline(surface, self.rayColor, debut, arret)
      except TypeError as oops:
        print(f"Failed at {debut} -> {arret}: {oops}!")
        self.die() # Unable to draw, therefore, life is forefeit.
        break

