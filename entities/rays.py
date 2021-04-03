

from attributes.living import Living
from attributes.moving import Moving2
from entities import Entity
from geometry.lines import Segment
from pygame.draw import line as aline, aaline
from random import random


RAY_MAXIMUM_BOUNCES = 4
RAY_MAXIMUM_LIFE = 2000
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


class Ray(Living, Moving2, Entity):
  def __init__(self, position, rayColor=None, trailLength=RAY_TRAIL_LENGTH):
    Moving2.__init__(self, position, (random() - 0.5, random() - 0.5))
    
    self.lastPosition = None
    self.rayColor = rayColor if rayColor else (int(random() * 255), int(random() * 255), int(random() * 255))
    self.life = int(random() * RAY_MAXIMUM_LIFE)
    # self.life = RAY_MAXIMUM_LIFE
    self.trail = list()
    self.trailLength = trailLength if 0 <= trailLength <= RAY_TRAIL_LENGTH else MAXIMUM_TRAIL_LENGTH

  def alive(self):
    return 0 < self.life

  def onReflection(self):
    pass # Do nothing, for now.

  def live(self, **kwargs):
    space = kwargs["space"] if "space" in kwargs else None

    if space:
      # Track only the last few positions.
      self.trail = self.trail[:-(self.trailLength - 1)]

      self.lastPosition = self.position
      lastVelocity = self.velocity

      # Reflect the ray if necessary.
      px, vx = reflect(0, self.position.x, self.velocity.x, space[0])
      py, vy = reflect(0, self.position.y, self.velocity.y, space[1])

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
      self.life -= 1
      
      # Add the latest segement.
      self.trail.append(Segment(self.lastPosition, self.position))

  def update(self, **kwargs):
    if self.alive():
      self.live(**kwargs)

  def draw(self, surface):
    for segment in self.trail:
      debut = segment.debut.tupled()
      arret = segment.arret.tupled()
      try:
        aline(surface, self.rayColor, debut, arret)
        # aaline(surface, self.rayColor, debut, arret)
      except TypeError as oops:
        print(f"Failed at {debut} -> {arret}: {oops}!")
        self.life = 0 # Unable to draw, therefore, life is forefeit.
        break


class BouncingRay(Ray):
  def __init__(self, position, bounces, trailLength=RAY_TRAIL_LENGTH):
    Ray.__init__(self, position, rayColor=(127, 127, 0), trailLength=trailLength)
    # It's life is based on bounces.
    self.bounces = bounces

  def alive(self):
    # Ensure life remains neutral.
    self.life = 0
    return 0 < self.bounces

  def onReflection(self):
    self.bounces -= 1

