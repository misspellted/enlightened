

from attributes.updated import Updated


class Environment(Updated):
  def __init__(self, timer):
    self.entities = list()
    self.timer = timer
    self.lastTime = timer.getTime()

  def update(self, **kwargs):
    print("hi")
    msDeltaTime = self.timer.update(**kwargs)

    # Send an update with delta time to all entities in the environment.
    for entity in self.entities:
      if entity.alive():
        entity.update(
          **kwargs,
          environment=self,
          deltaTime=msDeltaTime
        )

    # Remove any entities no longer alive.
    self.entities = [entity for entity in self.entities if entity.alive()]

