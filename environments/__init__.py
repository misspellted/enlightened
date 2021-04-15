

from attributes.updated import Updated


class Environment(Updated):
  def __init__(self, timer):
    self.timer = timer
    self.entities = list()

  def addEntity(self, entity):
    if not entity in self.entities:
      self.entities.append(entity)

  def update(self, **kwargs):
    print("hi")
    deltaTime = self.timer.update(**kwargs)

    # Remove any entities no longer alive.
    self.entities = [entity for entity in self.entities if entity.alive()]

    # Send an update with delta time to all entities in the environment.
    for entity in self.entities:
      if entity.alive():
        entity.update(**kwargs, environment=self, deltaTime=deltaTime)

