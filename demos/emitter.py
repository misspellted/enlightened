

from attributes.updated import Updated
from demos import PyGameApp, PyGameCursor
from geometry.vertices import Vertex2
import pygame
from random import random
from scenes.pygame import PyGameScene


RAY_TRAIL_LENGTH = 500
# MAXIMUM_RAYS = 16
# RAYS_PER_EMIT = MAXIMUM_RAYS >> 2
# EMIT_COOLDOWN = RAYS_PER_EMIT << 8
# TODO: Have fun with these! Definitely a particle system in this code, lol!
MAXIMUM_RAYS = 1024
RAYS_PER_EMIT = MAXIMUM_RAYS >> 2
EMIT_COOLDOWN = RAYS_PER_EMIT >> 1
# MAXIMUM_RAYS = 2
# RAYS_PER_EMIT = MAXIMUM_RAYS >> 1
# EMIT_COOLDOWN = RAYS_PER_EMIT << 8


class Ray:
  MAXIMUM_LIFE = 2000

  @staticmethod
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

  def __init__(self, position):
    self.lastPosition = None
    self.position = position
    self.velocity = (random() - 0.5, random() - 0.5)
    #self.rayColor = (127, 127, 0)
    self.rayColor = (int(random() * 255), int(random() * 255), int(random() * 255))
    self.life = int(random() * Ray.MAXIMUM_LIFE)
    # self.life = Ray.MAXIMUM_LIFE
    self.trail = list()

  def alive(self):
    return 0 < self.life

  def update(self, space):
    if 0 < self.life:
      self.lastPosition = self.position
      px, py = self.position
      vx, vy = self.velocity

      # print(f"[{vx, vy}] @ ({px}, {py})")

      # Reflect the ray if necessary.
      px, vx = Ray.reflect(0, px, vx, space[0])
      py, vy = Ray.reflect(0, py, vy, space[1])

      # print(f"[{vx, vy}] @ ({px}, {py})")

      self.position = (px, py)
      self.velocity = (vx, vy)
      self.life -= 1

  def draw(self, surface):
    try:
      pygame.draw.line(surface, self.rayColor, self.lastPosition, self.position)
      self.trail.append((self.lastPosition, self.position))
    except TypeError as oops:
      print(f"Failed at {self.lastPosition} -> {self.position}!")
      pass


class EmittingCursor(PyGameCursor):
  COLOR_EMITTING = (127, 0, 0) # 'R' for ... ?
  COLOR_GRABBING = (0, 127, 0) # 'G' for grab!
  COLOR_BOUNCING = (0, 0, 127) # 'B' for blue!

  def __init__(self, cameraOverlay, radius=20, cursorVisible=True):
    PyGameCursor.__init__(self, cameraOverlay, radius=radius, cursorVisible=cursorVisible)
    self.emitCoolDown = 0

  def bounce(self):
    # Use the cursor to indicate the 'bounce' mode.
    self.color = EmittingCursor.COLOR_BOUNCING

  def emit(self, raysPerEmit=RAYS_PER_EMIT):
    # Use the cursor to indicate the 'emit' mode.
    self.color = EmittingCursor.COLOR_EMITTING
    emitted = list()
    # Generate a bunch of Rays at the current position.
    if self.emitCoolDown <= 0:
      while len(emitted) < raysPerEmit: # len(emitted) < EmittingDemo.MAXIMUM_RAYS: # and emitted < EmittingDemo.RAYS_PER_EMIT:
        emitted.append(Ray(self.position.tupled()))
      self.emitCoolDown = EMIT_COOLDOWN
    return emitted

  def grab(self):
    # Use the cursor to indicate the 'grab' mode.
    self.color = EmittingCursor.COLOR_GRABBING

  def update(self):
    PyGameCursor.update(self)
    if 0 < self.emitCoolDown:
      self.emitCoolDown -= 1


class EmittingScene(PyGameScene, Updated):
  def __init__(self, length, height):
    PyGameScene.__init__(self, length, height)
    self.bouncing = True
    self.emitting = False
    self.grabbing = False
    self.wiping = False
    self.rays = list()

  def onMouseButtonDown(self, event):
    handled = False

    if event.button == pygame.BUTTON_LEFT:
      self.emitting = True
      handled = True
    elif event.button == pygame.BUTTON_RIGHT:
      self.grabbing = True
      handled = True
    elif event.button == pygame.BUTTON_MIDDLE:
      self.wiping = True
      handled = True

    return handled

  def onMouseButtonUp(self, event):
    handled = False

    if event.button == pygame.BUTTON_LEFT:
      self.emitting = False
      handled = True
    elif event.button == pygame.BUTTON_RIGHT:
      self.grabbing = False
      handled = True
    elif event.button == pygame.BUTTON_MIDDLE:
      self.wiping = False
      handled = True

    return handled
  
  def emitRays(self, cursorPosition):
    # Only have 16 rays maximum at a time.
    # And only emit so many per time.
    emitted = 0
    while emitted < RAYS_PER_EMIT: # len(self.rays) < EmittingDemo.MAXIMUM_RAYS: # and emitted < EmittingDemo.RAYS_PER_EMIT:
      self.rays.append(Ray(cursorPosition))
      emitted += 1
    return emitted

  def update(self, **kwargs):
    if self.wiping:
      self.scene.fill((0, 0, 0))

    cursor = kwargs["cursor"] if "cursor" in kwargs else None

    if cursor:
      if self.bouncing:
        cursor.bounce()
        # TODO: Bounce any existing rays hitting the cursor in bounce 'mode'.
      if self.emitting:
        self.rays.extend(cursor.emit()) # Add more rays...
        self.rays = self.rays[:MAXIMUM_RAYS] # .. but only allow up to a maximum.
      if self.grabbing:
        cursor.grab()
        # TODO: grab any rays hitting the cursor in grab 'mode'.

      for ray in self.rays:
        ray.update(self.dimensions.tupled())

        if (RAY_TRAIL_LENGTH - 1) < len(ray.trail):
          pygame.draw.line(self.scene, (0, 0, 0), ray.trail[-RAY_TRAIL_LENGTH][0], ray.trail[-RAY_TRAIL_LENGTH][0])
          # pygame.draw.aaline(self.scene, (0, 0, 0), ray.trail[-RAY_TRAIL_LENGTH][0], ray.trail[-RAY_TRAIL_LENGTH][0])

        ray.draw(self.scene)

      self.rays = [ray for ray in self.rays if ray.alive()]


class EmittingDemo(PyGameApp):
  def __init__(self):
    PyGameApp.__init__(self)
    self.scene = None
    self.cameraSensor = None
    self.baseCaption = "Emitter Demo"

  def onCameraOverlayConfigured(self, cameraOverlay):
    self.cursor = EmittingCursor(self.camera.overlay, cursorVisible=self.cursorVisible)

  def onCameraSensorConfigured(self, cameraSensor):
    self.scene = EmittingScene(*cameraSensor.dimensions.tupled())
    self.cameraSensor = cameraSensor

  def onMouseButtonDown(self, event):
    return False if not self.scene else self.scene.onMouseButtonDown(event)

  def onMouseButtonUp(self, event):
    return False if not self.scene else self.scene.onMouseButtonUp(event)

  def update(self):
    PyGameApp.update(self)

    rendering = None

    if self.scene:
      self.scene.update(cursor=self.cursor)
      rendering = self.scene.render()
      self.captionSuffix = f" - {len(self.scene.rays)} ray(s)"

    if self.cameraSensor and rendering:
      self.cameraSensor.displayRendering(rendering, Vertex2(0, 0))

