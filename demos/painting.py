
from demos import PyGameDemo
import pygame

class PaintingDemo(PyGameDemo):
  def __init__(self):
    PyGameDemo.__init__(self)
    self.cursorPosition = None
    self.cursorColor = (127, 127, 127)
    self.cursorRadius = 20
    self.cursorRect = None
    self.lastCursorRect = None
    self.lastCursorArea = None
    self.painting = False
    self.paintColor = (127, 0, 0)
    self.erasing = False
    self.eraseColor = (0, 0, 0)

  def processEvent(self, event):
    if event.type == pygame.MOUSEMOTION:
      self.cursorPosition = event.pos
    elif event.type == pygame.MOUSEBUTTONDOWN:
      if event.button == pygame.BUTTON_LEFT:
        self.painting = True
      elif event.button == pygame.BUTTON_RIGHT:
        self.erasing = True
      else:
        PyGameDemo.processEvent(self, event)
    elif event.type == pygame.MOUSEBUTTONUP:
      if event.button == pygame.BUTTON_LEFT:
        self.painting = False
      elif event.button == pygame.BUTTON_RIGHT:
        self.erasing = False
      else:
        PyGameDemo.processEvent(self, event)
    else:
      PyGameDemo.processEvent(self, event)

  def update(self):
    # Redraw where the last cursor was.
    if self.lastCursorRect is not None:
      self.window.blit(self.lastCursorArea, self.lastCursorRect)

    if self.cursorPosition is not None:
      # Draw a circle any time we're "painting" or "erasing".
      if self.painting:
        pygame.draw.circle(self.window, self.paintColor, self.cursorPosition, self.cursorRadius, 1)
      elif self.erasing:
        pygame.draw.circle(self.window, self.eraseColor, self.cursorPosition, self.cursorRadius, 1)

      # Capture the area under where the cursor would be drawn.
      self.cursorRect = pygame.Rect(0, 0, self.cursorRadius * 2, self.cursorRadius * 2)
      self.cursorRect.center = self.cursorPosition

      # Stay within the bounds of the window.
      if self.cursorRect.left < 0: self.cursorRect.left = 0
      if self.windowDimensions[0] < self.cursorRect.right: self.cursorRect.right = self.windowDimensions[0]
      if self.cursorRect.top < 0: self.cursorRect.top = 0
      if self.windowDimensions[1] < self.cursorRect.bottom: self.cursorRect.bottom = self.windowDimensions[1]

      self.lastCursorRect = self.cursorRect.copy()
      self.lastCursorArea = self.window.subsurface(self.cursorRect).copy()

      # Then draw the cursor.
      pygame.draw.circle(self.window, self.cursorColor, self.cursorPosition, self.cursorRadius, 1)

    PyGameDemo.update(self)
