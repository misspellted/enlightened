

from attributes.updated import Updated
from demos import PyGameApp, PyGameCursor, DEMO_WINDOW_LENGTH, DEMO_WINDOW_HEIGHT
from entities.rays import Ray
from geometry.vertices import Vertex2
import pygame
from scenes.pygame import PyGameScene


# TODO: Have fun with these! Definitely a particle system in this code, lol!
MAXIMUM_RAYS = 10240
RAYS_PER_EMIT = MAXIMUM_RAYS >> 3
EMIT_COOLDOWN = 1 << 3


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

  def emitRay(self):
    return Ray(self.position.tupled())

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
        ray.update(space=self.dimensions.tupled())

      self.rays = [ray for ray in self.rays if ray.alive()]

      for ray in self.rays:
        ray.draw(self.scene)


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


# This demo can be invoked directly, using the following command while in the
#   directory of the repository:
#
#     python -m demos.emitter
if __name__ == "__main__":
  demo = EmittingDemo()
  demo.run(DEMO_WINDOW_LENGTH, DEMO_WINDOW_HEIGHT, False)
  del demo

