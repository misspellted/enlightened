

from attributes.living import Living
import pygame
from random import random


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


class Ray:
  def __init__(self, position, rayColor=None):
    self.lastPosition = None
    self.position = position
    self.velocity = (random() - 0.5, random() - 0.5)
    self.rayColor = rayColor if rayColor else (int(random() * 255), int(random() * 255), int(random() * 255))
    self.life = int(random() * RAY_MAXIMUM_LIFE)
    # self.life = RAY_MAXIMUM_LIFE
    self.trail = list()

  def alive(self):
    return 0 < self.life

  def onReflection(self):
    pass # Do nothing, for now.

  def live(self, **kwargs):
    space = kwargs["space"] if "space" in kwargs else None

    if space:
      # Track only the last few positions.
      self.trail = self.trail[:-(RAY_TRAIL_LENGTH - 1)]

      self.lastPosition = self.position
      px, py = self.position
      lvx, lvy = self.velocity

      # print(f"[{lvx, lvy}] @ ({px}, {py})")

      # Reflect the ray if necessary.
      px, nvx = reflect(0, px, lvx, space[0])
      py, nvy = reflect(0, py, lvy, space[1])

      if lvx != nvx or lvy != nvy:
        self.onReflection()

      # print(f"[{nvx, nvy}] @ ({px}, {py})")

      self.position = (px, py)
      self.velocity = (nvx, nvy)
      self.life -= 1
      
      # Add the latest segement.
      self.trail.append((self.lastPosition, self.position))

  def update(self, space):
    if self.alive():
      self.live(space=space)

  def draw(self, surface):
    for segment in self.trail:
      try:
        pygame.draw.line(surface, self.rayColor, segment[0], segment[1])
        # pygame.draw.aaline(surface, self.rayColor, segment[0], segment[1])
      except TypeError as oops:
        print(f"Failed at {segment[0]} -> {segment[1]}!")
        self.life = 0 # Unable to draw, therefore, life is forefeit.
        break

