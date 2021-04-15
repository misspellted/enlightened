
from applications.pygame import PyGameApplication
from defaults import DEMO_WINDOW_LENGTH, DEMO_WINDOW_HEIGHT
from emitter import EmittingCursor
from entities.rays import Ray
from geometry.vertices import Vertex2
import pygame
from random import random
from scenes.pygame import PyGameScene
from timers.python import PythonSeconds


# TODO: Have fun with these! Definitely a particle system in this code, lol!
MAXIMUM_RAYS = 16
RAYS_PER_EMIT = MAXIMUM_RAYS >> 2
EMIT_COOLDOWN = 1 << 3


class BouncingCursor(EmittingCursor):
  def __init__(self, cameraOverlay, radius=20, mouseVisible=True):
    EmittingCursor.__init__(self, cameraOverlay, radius=radius, mouseVisible=mouseVisible)

  def emitRay(self):
    return Ray(self.position.copy(), Vertex2(random() - 0.5, random() - 0.5), rayColor=(127, 127, 0))


class BouncingScene(PyGameScene):
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


class BouncerDemo(PyGameApplication):
  def __init__(self, length, height, mouseVisible=True):
    PyGameApplication.__init__(self, length, height, timer=PythonSeconds(), mouseVisible=mouseVisible)
    self.setCursor(BouncingCursor(self.camera.overlay, mouseVisible=mouseVisible))
    self.setEnvironment(BouncingScene(self.timer, length, height))
    self.captionWindow("Bouncer Demo")


if __name__ == "__main__":
  demo = BouncerDemo(DEMO_WINDOW_LENGTH, DEMO_WINDOW_HEIGHT, False)
  demo.run()
  del demo

