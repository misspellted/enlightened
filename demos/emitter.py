
from demos import PyGameDemo
import pygame

class EmittingDemo(PyGameDemo):
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
      cursorColor = self.cursorColor # Default - TODO: Make the emitted rays bounce off the cursor.
      if self.emitting:
        cursorColor = self.emitColor
      elif self.absorbing:
        cursorColor = self.absorbColor

      pygame.draw.circle(self.window, cursorColor, self.cursorPosition, self.cursorRadius, 1)

      # TODO: Emit rays.
      # TODO: Bounce rays.
      # TODO: Grab rays.

    PyGameDemo.update(self)
