
from attributes.rendered import Rendered
from demos import PyGameApp, PyGameCursor
from emissions.rays import Ray
from geometry.vertices import Vertex2
from random import random
import pygame


MAXIMUM_LIFE = 2000
MAXIMUM_BOUNCES = 2


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


class BouncingRay(Ray):
  def __init__(self, bounces, position, rayColor):
    # A bouncing ray doesn't have a simple evolution-based life.
    # It's life is based on bounces.
    Ray.__init__(self, MAXIMUM_LIFE, position, rayColor)
    self.bounces = bounces

  # def alive(self):
  #   return 0 < self.bounces


class BouncingDemo(PyGameApp):
  # RAYS_PER_EMIT = MAXIMUM_RAYS >> 2
  # EMIT_COOLDOWN = RAYS_PER_EMIT << 8
  # TODO: Have fun with these! Definitely a particle system in this code, lol!
  MAXIMUM_RAYS = 128
  RAYS_PER_EMIT = MAXIMUM_RAYS >> 4
  EMIT_COOLDOWN = 32 #RAYS_PER_EMIT << 1
  # RAYS_PER_EMIT = 1
  # EMIT_COOLDOWN = 32

  def __init__(self):
    PyGameApp.__init__(self)
    self.cursor = BRCursor(10)
    self.cursorPosition = None
    self.lastCursorRect = None
    self.lastCursorArea = None
    self.emitting = False
    self.emitColor = (127, 0, 0) # Red for emit
    self.absorbing = False
    self.absorbColor = (0, 127, 0) # Green for 'grab'/absorb
    self.rays = list() # Track the rays in the scene.
    self.emitCoolDown = 0
    self.wiping = False
    self.buffer = None
    self.lastRayCount = 0

  def onViewerDimensioned(self, length, height):
    print(f"Viewer dimensions: ({length}, {height})")
    self.buffer = Buffer(length, height)

  def onMouseButtonDown(self, event):
    handled = False

    if event.button == pygame.BUTTON_LEFT:
      self.cursor.emit()
      self.emitting = True
      handled = True
    elif event.button == pygame.BUTTON_RIGHT:
      self.cursor.grab()
      self.absorbing = True
      handled = True
    elif event.button == pygame.BUTTON_MIDDLE:
      self.wiping = True
      handled = True

    return handled

  def onMouseButtonUp(self, event):
    handled = False

    if event.button == pygame.BUTTON_LEFT:
      self.cursor.bounce()
      self.emitting = False
      handled = True
    elif event.button == pygame.BUTTON_RIGHT:
      self.cursor.bounce()
      self.absorbing = False
      handled = True
    elif event.button == pygame.BUTTON_MIDDLE:
      self.wiping = False
      handled = True

    return handled
  
  def emitRays(self, cursorPosition):
    # Only have 16 rays maximum at a time.
    # And only emit so many per time.
    emitted = 0
    while len(self.rays) < BouncingDemo.MAXIMUM_RAYS and emitted < BouncingDemo.RAYS_PER_EMIT:
      self.rays.append(BouncingRay(MAXIMUM_LIFE, cursorPosition, (int(random() * 255), int(random() * 255), int(random() * 255))))
      emitted += 1
    return emitted

  def update(self):#, msTimeSinceStart):
    # First, wipe the buffer, if it was requested.
    # if self.wiping:
    self.buffer.wipe()

    # TODO: Absorb any rays hitting the cursor in absorb 'mode'.

    # TODO: Bounce any existing rays hitting the cursor in bounce 'mode'.

    # Emit new rays when the cursor is in emit 'mode'.
    if self.emitting:
      if self.emitCoolDown <= 0:
        emitted = self.emitRays(self.cursor.position.tupled())
        if 0 < emitted:
          self.emitCoolDown = BouncingDemo.EMIT_COOLDOWN
          #print(f"Emitted {emitted} ray(s).")
      else:
        self.emitCoolDown -= 1

    if len(self.rays) != self.lastRayCount:
      self.lastRayCount = len(self.rays)
      print(f"Drawing {self.lastRayCount} ray(s)")

    debutTicks = pygame.time.get_ticks()
    for ray in self.rays:
      ray.update(space=self.buffer.dimensions)
      ray.draw(self.buffer)
    arretTicks = pygame.time.get_ticks()
    print(f"Took {arretTicks - debutTicks} tick(s) to draw {len(self.rays)} ray(s).")

    # Draw the cursor.
    debutTicks = pygame.time.get_ticks()
    rendered = self.cursor.render()
    cursorRect = rendered.get_rect()
    cursorRect.center = self.cursor.position.tupled() 
    self.buffer.blit(rendered, cursorRect, special_flags=pygame.BLEND_ALPHA_SDL2)
    arretTicks = pygame.time.get_ticks()
    print(f"Took {arretTicks - debutTicks} tick(s) to draw the curosr.")

    self.rays = [ray for ray in self.rays if ray.alive()]

    self.viewer.blit(self.buffer, (0, 0))

    PyGameApp.update(self)

  def run(self, windowLength, windowHeight):
    PyGameApp.run(self, windowLength, windowHeight, False) # Hide the cursor for this demo.

