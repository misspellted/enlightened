
from demos import PyGameDemo
from random import random
import pygame

class Ray:
  MAXIMUM_LIFE = 2000

  def __init__(self, position):
    self.lastPosition = None
    self.position = position
    self.velocity = (random(), random())
    self.rayColor = (127, 127, 0)
    self.life = int(random() * Ray.MAXIMUM_LIFE)
    self.trail = list()

  def update(self, space):
    if 0 < self.life:
      self.lastPosition = self.position
      px, py = self.position
      vx, vy = self.velocity
      if not 0 <= px < space[0]:
        vx *= -1
      if not 0 <= py < space[1]:
        vy *= -1
      px += vx
      py += vy
      self.position = (px, py)
      self.velocity = (vx, vy)
      self.life -= 1

  def draw(self, surface):
    pygame.draw.line(surface, self.rayColor, self.lastPosition, self.position)
    self.trail.append((self.lastPosition, self.position))

class EmittingDemo(PyGameDemo):
  MAXIMUM_RAYS = 16
  RAYS_PER_EMIT = MAXIMUM_RAYS >> 2
  EMIT_COOLDOWN = RAYS_PER_EMIT << 8

  def __init__(self):
    PyGameDemo.__init__(self)
    self.cursorPosition = None
    self.cursorColor = (0, 0, 127) # Blue for 'bounce'
    self.cursorRadius = 10
    self.cursorRect = None
    self.lastCursorRect = None
    self.lastCursorArea = None
    self.emitting = False
    self.emitColor = (127, 0, 0) # Red for emit
    self.absorbing = False
    self.absorbColor = (0, 127, 0) # Green for 'grab'/absorb
    self.rays = list() # Track the rays in the scene.
    self.emitCoolDown = 0

  def createWindow(self, length, height):
    PyGameDemo.createWindow(self, length, height)
    # Hide the mouse cursor for this demo.
    pygame.mouse.set_visible(False)

  def processEvent(self, event):
    if event.type == pygame.MOUSEMOTION:
      self.cursorPosition = event.pos
    elif event.type == pygame.MOUSEBUTTONDOWN:
      if event.button == pygame.BUTTON_LEFT:
        self.emitting = True
      elif event.button == pygame.BUTTON_RIGHT:
        self.absorbing = True
      else:
        PyGameDemo.processEvent(self, event)
    elif event.type == pygame.MOUSEBUTTONUP:
      if event.button == pygame.BUTTON_LEFT:
        self.emitting = False
      elif event.button == pygame.BUTTON_RIGHT:
        self.absorbing = False
      else:
        PyGameDemo.processEvent(self, event)
    else:
      PyGameDemo.processEvent(self, event)
  
  def emitRays(self, cursorPosition):
    # Only have 16 rays maximum at a time.
    # And only emit so many per time.
    emitted = 0
    while len(self.rays) < EmittingDemo.MAXIMUM_RAYS and emitted < EmittingDemo.RAYS_PER_EMIT:
      self.rays.append(Ray(cursorPosition))
      emitted += 1
    return emitted

  def update(self):
    # Redraw where the last cursor was.
    if self.lastCursorRect is not None:
      self.window.blit(self.lastCursorArea, self.lastCursorRect)

    if self.cursorPosition is not None:
      # Capture the area under where the cursor would be drawn.
      self.cursorRect = pygame.Rect(0, 0, self.cursorRadius * 2, self.cursorRadius * 2)
      self.cursorRect.center = self.cursorPosition

      # Stay within the bounds of the window.
      self.cursorRect.clamp_ip(0, 0, self.windowDimensions[0], self.windowDimensions[1])
      
      self.lastCursorRect = self.cursorRect.copy()
      self.lastCursorArea = self.window.subsurface(self.cursorRect).copy()

      # The cursor color is dependent on the state of the demo.
      cursorColor = self.cursorColor
      if self.emitting:
        cursorColor = self.emitColor
      elif self.absorbing:
        cursorColor = self.absorbColor

      pygame.draw.circle(self.window, cursorColor, self.cursorPosition, self.cursorRadius, 1)

      # TODO: Absorb any rays hitting the cursor in absorb 'mode'.

      # TODO: Bounce any existing rays hitting the cursor in bounce 'mode'.

      # Emit new rays when the cursor is in emit 'mode'.
      if self.emitting:
        if self.emitCoolDown <= 0:
          emitted = self.emitRays(self.cursorPosition)
          if 0 < emitted:
            self.emitCoolDown = EmittingDemo.EMIT_COOLDOWN
            #print(f"Emitted {emitted} ray(s).")
        else:
          self.emitCoolDown -= 1

      for ray in self.rays:
        ray.update(self.window.get_size())

        if 0 < len(ray.trail):
          pygame.draw.line(self.window, (0, 0, 0), ray.trail[-1][0], ray.trail[-1][0])

        ray.draw(self.window)

      self.rays = [ray for ray in self.rays if 0 < ray.life]

    PyGameDemo.update(self)
