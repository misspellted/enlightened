

from applications.pygame import PyGameApplication
from cursors.pygame import PyGameCursor
from defaults import DEMO_WINDOW_LENGTH, DEMO_WINDOW_HEIGHT
from entities.rays import Ray
from geometry.vertices import Vertex2
from math import cos, sin, pi
import pygame
from random import random
from scenes.pygame import PyGameScene


# TODO: Have fun with these! Definitely a particle system in this code, lol!
MAXIMUM_RAYS = 10240
RAYS_PER_EMIT = MAXIMUM_RAYS >> 3
EMIT_COOLDOWN = 1 << 3


class EmittingCursor(PyGameCursor):
  COLOR_EMITTING = (127, 0, 0) # 'R' for ... ?
  COLOR_GRABBING = (0, 127, 0) # 'G' for grab!
  COLOR_BOUNCING = (0, 0, 127) # 'B' for blue!

  def __init__(self, cameraOverlay, radius=20, mouseVisible=True):
    PyGameCursor.__init__(self, cameraOverlay, radius=radius, mouseVisible=mouseVisible)
    self.emitCoolDown = 0

  def bounce(self):
    # Use the cursor to indicate the 'bounce' mode.
    self.color = EmittingCursor.COLOR_BOUNCING

  def emitRay(self):
    return Ray(self.position.copy(), Vertex2(random() - 0.5, random() - 0.5))

  def emitRays(self, raysPerEmit):
    # Use the cursor to indicate the 'emit' mode.
    self.color = EmittingCursor.COLOR_EMITTING
    emitted = list()
    # Generate a bunch of rays at the current position.
    if self.emitCoolDown <= 0:
      while len(emitted) < raysPerEmit:
        emitted.append(self.emitRay())
      self.emitCoolDown = EMIT_COOLDOWN
    return emitted

  def grab(self):
    # Use the cursor to indicate the 'grab' mode.
    self.color = EmittingCursor.COLOR_GRABBING

  def update(self, **kwargs):
    PyGameCursor.update(self, **kwargs)
    if 0 < self.emitCoolDown:
      self.emitCoolDown -= 1


class EmittingScene(PyGameScene):
  def __init__(self, timer, length, height):
    PyGameScene.__init__(self, timer, length, height)
    self.bouncing = True
    self.emitting = False
    self.grabbing = False
    self.wiping = False
    self.rays = list()

  def onMouseButtonPressed(self, button):
    handled = False

    if button == pygame.BUTTON_LEFT:
      self.emitting = True
      handled = True
    elif button == pygame.BUTTON_RIGHT:
      self.grabbing = True
      handled = True
    elif button == pygame.BUTTON_MIDDLE:
      self.wiping = True
      handled = True

    return handled

  def onMouseButtonReleased(self, button):
    handled = False

    if button == pygame.BUTTON_LEFT:
      self.emitting = False
      handled = True
    elif button == pygame.BUTTON_RIGHT:
      self.grabbing = False
      handled = True
    elif button == pygame.BUTTON_MIDDLE:
      self.wiping = False
      handled = True

    return handled

  def update(self, **kwargs):
    if self.wiping:
      self.scene.fill((0, 0, 0))

    cursor = kwargs["cursor"] if "cursor" in kwargs else None

    if cursor:
      if self.bouncing:
        cursor.bounce()
        # TODO: Bounce any existing rays hitting the cursor in bounce 'mode'.
      if self.emitting:
        self.rays.extend(cursor.emitRays(RAYS_PER_EMIT)) # Add more rays...
        self.rays = self.rays[:MAXIMUM_RAYS] # .. but only allow up to a maximum.
      if self.grabbing:
        cursor.grab()
        # TODO: grab any rays hitting the cursor in grab 'mode'.

    for ray in self.rays:
      ray.update(**kwargs, environment=self)

    self.rays = [ray for ray in self.rays if ray.alive()]

    for ray in self.rays:
      ray.draw(self.scene)


class EmittingDemo(PyGameApplication):
  def __init__(self, length, height, mouseVisible=True):
    PyGameApplication.__init__(self, length, height, mouseVisible=mouseVisible)
    self.setCursor(EmittingCursor(self.camera.overlay, mouseVisible=mouseVisible))
    self.setEnvironment(EmittingScene(self.timer, length, height))
    self.captionWindow("Emitter Demo")


if __name__ == "__main__":
  demo = EmittingDemo(DEMO_WINDOW_LENGTH, DEMO_WINDOW_HEIGHT, False)
  demo.run()
  del demo

