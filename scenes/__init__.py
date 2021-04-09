

from attributes.rendered import Rendered
from environments.planar import PlanarEnvironment


class Scene(PlanarEnvironment, Rendered):
  def __init__(self, timer, length, height):
    if length * height <= 0:
      raise ValueError(f"The dimensions of the scene are invalid: [{length}, {height}]")

    PlanarEnvironment.__init__(self, timer, (length, height))

