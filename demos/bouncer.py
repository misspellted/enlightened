
from attributes.rendered import Rendered
from demos import PyGameApp, PyGameCursor, DEMO_WINDOW_LENGTH, DEMO_WINDOW_HEIGHT
from demos.emitter import EmittingCursor
from entities.rays import BouncingRay, RAY_MAXIMUM_BOUNCES
from geometry.vertices import Vertex2
import pygame
from scenes.pygame import PyGameScene


# TODO: Have fun with these! Definitely a particle system in this code, lol!
MAXIMUM_RAYS = 16
RAYS_PER_EMIT = MAXIMUM_RAYS >> 2
EMIT_COOLDOWN = 1 << 3


class Buffer(pygame.Surface):
  def __init__(self, length, height):
    pygame.Surface.__init__(self, (length, height))

  @property
  def dimensions(self):
    return self.get_size()

  def wipe(self, color=(0, 0, 0)):
    self.fill(color)


class BRCursor(PyGameCursor, Rendered):
  COLOR_BOUNCE = (0, 0, 127)
  COLOR_GRAB = (0, 127, 0)
  COLOR_EMIT = (127, 0, 0)

  def __init__(self, radius):
    PyGameCursor.__init__(self)
    self.radius = radius
    self.bounce()

  def bounce(self):
    self.color = BRCursor.COLOR_BOUNCE

  def emit(self):
    self.color = BRCursor.COLOR_EMIT

  def grab(self):
    self.color = BRCursor.COLOR_GRAB

  def render(self):
    rendering = pygame.Surface((self.radius * 2, self.radius * 2))
    pygame.draw.circle(rendering, self.color, (self.radius, self.radius), self.radius, 1)
    return rendering


class BouncingCursor(EmittingCursor):
  def __init__(self, cameraOverlay, radius=20, cursorVisible=True):
    EmittingCursor.__init__(self, cameraOverlay, radius=radius, cursorVisible=cursorVisible)

  def emitRay(self):
    return BouncingRay(self.position.tupled(), RAY_MAXIMUM_BOUNCES)


class BouncingScene(PyGameScene):
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


class BouncingDemo(PyGameApp):
  def __init__(self):
    PyGameApp.__init__(self)
    self.scene = None
    self.cameraSensor = None
    self.baseCaption = "Bouncer Demo"

  def onCameraOverlayConfigured(self, cameraOverlay):
    self.cursor = BouncingCursor(self.camera.overlay, cursorVisible=self.cursorVisible)

  def onCameraSensorConfigured(self, cameraSensor):
    self.scene = BouncingScene(*cameraSensor.dimensions.tupled())
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
#     python -m demos.bouncer
if __name__ == "__main__":
  demo = BouncingDemo()
  demo.run(DEMO_WINDOW_LENGTH, DEMO_WINDOW_HEIGHT, False)
  del demo

