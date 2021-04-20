

class Event:
  def __init__(self, type, source, **kwargs):
    self.type = type
    self.source = source
    self.details = dict(**kwargs)


class EventHandler:
  def handle(self, event):
    print(event) # Just .. log the event.
    return True

