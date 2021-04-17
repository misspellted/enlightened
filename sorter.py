

from algorithms.sorting.bubble import BubbleSort
from applications.pygame import PyGameApplication
from attributes.intervaled import Intervaled
from cursors.pygame import PyGameCursor
from defaults import DEMO_WINDOW_LENGTH, DEMO_WINDOW_HEIGHT
from geometry.vertices import Vertex2
from math import radians, cos, sin, floor
import pygame
from pygame.draw import line as aline, aaline
from random import randint
from scenes.pygame import PyGameScene
from units.prefixes.small import Milli


DATA_SIZE = 360


class SortingScene(PyGameScene, Intervaled):
  def __init__(self, timer, length, height, algorithm):
    PyGameScene.__init__(self, timer, length, height)
    resolution = Milli()
    Intervaled.__init__(self, 1 / (resolution.scalor * 120), resolution)
    self.origin = Vertex2(length / 2, height / 2)
    self.radius = min(*self.origin.coordinates) * 0.80
    self.algorithm = algorithm
    self.reset()

  def shuffle(self, shuffles=3000):
    count = 0
    while count < shuffles:
      a = randint(0, len(self.data) - 1)
      b = randint(0, len(self.data) - 1)

      if a != b:
        self.data[a], self.data[b] = self.data[b], self.data[a]
        count += 1

  def reset(self):
    self.data = list(range(DATA_SIZE))
    self.shuffle()
    self.algorithm.reset()
    self.delayed = False

  def onMouseButtonPressed(self, button):
    handled = False

    if button == pygame.BUTTON_LEFT:
      # Only allow a shuffle if the algorithm is finished.
      if self.algorithm.finished(self.data):
        if not self.delayed:
          self.delayed = True
        else:
          self.reset()
      handled = True

    return handled

  def radialize(self, value):
    return radians((value - 0) / (len(self.data) - 0) * 360)

  def colorize(self, value):
    # Based on https://www.particleincell.com/2014/colormap/ (the "Long Rainbow")
    f = (value - 0) / (len(self.data) - 0)

    a = (1 - f) / 0.2
    X = floor(a)
    Y = floor(255 * (a - X))

    r, g, b = 0, 0, 0

    if X == 0:
      r, g, b = 255, Y, 0
    elif X == 1:
      r, g, b = 255 - Y, 255, 0
    elif X == 2:
      r, g, b = 0, 255, Y
    elif X == 3:
      r, g, b = 0, 255 - Y, 255
    elif X == 4:
      r, g, b = Y, 0, 255
    else:
      r, g, b = 255, 0, 255

    return (r, g, b)

  def onInterval(self):
    self.data = self.algorithm.step(self.data)

  def update(self, **kwargs):
    self.scene.fill((0, 0, 0))

    Intervaled.update(self, **kwargs)

    length, height = self.dimensions.tupled()

    # Draw a line for each data point.
    for index in range(len(self.data)):
      point = self.data[index]
      rads = self.radialize(index)

      outer = self.origin + Vertex2(cos(rads) * length / 2, sin(rads) * height / 2)
      color = self.colorize(point)

      try:
        aaline(self.scene, color, self.origin.tupled(), outer.tupled())
        aline(self.scene, color, self.origin.tupled(), outer.tupled())
      except TypeError as oops:
        print(f"Failed at {origin} -> {outer}: {oops}!")
        break


class SorterDemo(PyGameApplication):
  def __init__(self, length, height, mouseVisible=True):
    PyGameApplication.__init__(self, length, height, mouseVisible=mouseVisible)
    self.setCursor(PyGameCursor(self.camera.overlay, mouseVisible=mouseVisible))
    algorithm = BubbleSort()
    self.setEnvironment(SortingScene(self.timer, length, height, BubbleSort()))
    self.captionWindow(f"Sorter Demo - {algorithm.name}")


if __name__ == "__main__":
  demo = SorterDemo(DEMO_WINDOW_LENGTH, DEMO_WINDOW_HEIGHT, False)
  demo.run()
  del demo

