

from attributes.moving import Moving
from attributes.positioned import Positioned
from entities import Entity
from geometry.lines import Segment
from pygame.draw import line as aline, aaline
from random import random
from units.prefixes.small import Milli


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


class Ray(Entity, Positioned, Moving):
  def __init__(self, position, velocity, rayColor=None, trailLength=RAY_TRAIL_LENGTH):
    Positioned.__init__(self, position)
    Moving.__init__(self, velocity)
    
    self.lastPosition = None
    self.rayColor = rayColor if rayColor else (int(random() * 255), int(random() * 255), int(random() * 255))
    self.bounces = RAY_BOUNCES
    self.trail = list()
    self.trailLength = trailLength if 0 <= trailLength <= RAY_TRAIL_LENGTH else MAXIMUM_TRAIL_LENGTH
    self.timeResolution = Milli()

  def alive(self):
    return 0 <= self.bounces

  def die(self):
    self.bounces = -1

  def onReflection(self):
    self.bounces -= 1

  def update(self, **kwargs):
    deltaTime = kwargs["deltaTime"] if "deltaTime" in kwargs else None
    environment = kwargs["environment"] if "environment" in kwargs else None

    velocityModifier = 1
    if deltaTime:
      velocityModifier = deltaTime.convertTo(self.timeResolution).magnitude

    modifiedVelocity = self.velocity * velocityModifier

    if environment:
      length, height = environment.dimensions.tupled()
      # Track only the last few positions.
      self.trail = self.trail[:-(self.trailLength - 1)]

      self.lastPosition = self.position

      # TODO: Use perception (do a perception check! lol) to determine
      # near-by entities that might cause interfere with the projection.

      # Project the ray's future position.
      # projected = self.projectBy(self.velocity)

      # Reflect the ray if necessary.
      px, vx = reflect(0, self.position.x, modifiedVelocity.x, length)
      py, vy = reflect(0, self.position.y, modifiedVelocity.y, height)

      if modifiedVelocity.x != vx or modifiedVelocity.y != vy:
        self.onReflection()

      if modifiedVelocity.x != vx:
        self.velocity.x *= -1

      if modifiedVelocity.y != vy:
        self.velocity.y *= -1

      self.position.x = px
      self.position.y = py
      
      # Add the latest segement.
      self.trail.append(Segment(self.lastPosition, self.position))

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

