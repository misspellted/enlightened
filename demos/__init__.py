
import pygame


class PyGameDemo:
  def __init__(self):
    pygame.init()

  def createWindow(self, length, height):
    self.window = pygame.display.set_mode((length, height))#.convert_alpha()
    self.windowDimensions = self.window.get_size()
    self.origin = (self.windowDimensions[0] // 2, self.windowDimensions[1] // 2)

  def processEvent(self, event):
    print(event)

  def update(self):
    pygame.display.flip()

  def terminate(self):
    pass

  def run(self, windowLength, windowHeight):
    self.createWindow(windowLength, windowHeight)
    
    running = True
    while running:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          running = False
        else:
          self.processEvent(event)
      
      if running:
        self.update()

  def __del__(self):
    pygame.quit()
    del self.window
