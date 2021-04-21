

from algorithms.sorting import SortingAlgorithm


class BubbleSort(SortingAlgorithm):
  def __init__(self):
    SortingAlgorithm.__init__(self, "Bubble Sort")
    self.reset()

  def reset(self):
    self.started = False
    self.swaps = 0

  def finished(self, data):
    return self.started and self.swaps == 0

  def step(self, data):
    if not self.started:
      self.started = True

    # One 'step' is one iteration through the elements.
    # Reset the swap count on every iteration.
    self.swaps = 0

    # Each iteration compares the current element with the next,
    # swapping if the current is larger than the next.

    for index in range(len(data) - 1):
      if data[index + 1] < data[index]:
        self.swaps += 1
        data[index], data[index + 1] = data[index + 1], data[index]

    return data


class OptimizedBubbleSort(BubbleSort):
  # The optimized version tracks how many steps taken, so that it need not
  # sort the largest element at the end of the collection again.
  def __init__(self):
    BubbleSort.__init__(self)
    self.name = "Bubble Sort (Optimized)"
    self.reset()

  def reset(self):
    BubbleSort.reset(self)
    self.steps = 0

  def step(self, data):
    if not self.started:
      self.started = True

    # One 'step' is one iteration through the elements.
    self.steps += 1

    # Reset the swap count on every iteration.
    self.swaps = 0

    # Each iteration compares the current element with the next,
    # swapping if the current is larger than the next.

    for index in range(len(data) - self.steps):
      if data[index + 1] < data[index]:
        self.swaps += 1
        data[index], data[index + 1] = data[index + 1], data[index]

    return data

