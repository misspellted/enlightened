

from algorithms.sorting import SortingAlgorithm


class BubbleSort(SortingAlgorithm):
  def __init__(self):
    SortingAlgorithm.__init__(self, "Bubble Sort")
    self.reset()

  def reset(self):
    self.sorted = 0

  def started(self, data):
    return 0 < self.sorted

  def finished(self, data):
    return self.sorted == len(data)

  def step(self, data):
    if not self.finished(data):
      targetIndex = len(data) - 1 - self.sorted
      highestIndex = 0
      highest = data[highestIndex]

      for index in range(targetIndex + 1):
        value = data[index]

        if not highest:
          highest = value
          highestIndex = index
        else:
          if highest < value:
            highest = value
            highestIndex = index

      data[targetIndex], data[highestIndex] = data[highestIndex], data[targetIndex]
      self.sorted += 1

    return data

