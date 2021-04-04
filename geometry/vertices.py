

class Vertex:
  def __init__(self, *coordinates):
    self.coordinates = list(coordinates)

  def tupled(self):
    return tuple(self.coordinates)

  def copy(self):
    return Vertex(*self.coordinates)

  def __eq__(self, other):
    equal = isinstance(other, Vertex)

    if equal:
      # True equality demands equal dimensions.
      equal = len(self.coordinates) == len(other.coordinates)
    
    if equal:
      for dimension in range(len(self.coordinates)):
        equal = self.coordinates[dimension] == other.coordinates[dimension]

        if not equal:
          break

    return equal

  # ================================
  # Translation Operations
  # ================================

  # self+addend
  def __add__(self, addend):
    if not isinstance(addend, Vertex):
      raise TypeError("Expected 'addend' to be an instance of Vertex!")
    dimensions = min(len(self.coordinates), len(addend.coordinates))
    return Vertex(*[self.coordinates[dimension] + addend.coordinates[dimension] for dimension in range(dimensions)])

  # augend+self
  def __radd__(self, augend):
    if not isinstance(augend, Vertex):
      raise TypeError("Expected 'augend' to be an instance of Vertex!")
    dimensions = min(len(augend.coordinates), len(self.coordinates))
    return Vertex(*[augend.coordinates[dimension] + self.coordinates[dimension] for dimension in range(dimensions)])

  # self+=addend
  def __iadd__(self, addend):
    if not isinstance(addend, Vertex):
      raise TypeError("Expected 'addend' to be an instance of Vertex!")
    for dimension in range(min(len(self.coordinates), len(addend.coordinates))):
      self.coordinates[dimension] += addend.coordinates[dimension]
    return self

  # self-subtrahend
  def __sub__(self, subtrahend):
    if not isinstance(subtrahend, Vertex):
      raise TypeError("Expected 'subtrahend' to be an instance of Vertex!")
    dimensions = min(len(self.coordinates), len(subtrahend.coordinates))
    return Vertex(*[self.coordinates[dimension] - subtrahend.coordinates[dimension] for dimension in range(dimensions)])

  # minuend-self
  def __rsub__(self, minuend):
    if not isinstance(minuend, Vertex):
      raise TypeError("Expected 'minuend' to be an instance of Vertex!")
    dimensions = min(len(minuend.coordinates), len(self.coordinates))
    return Vertex(*[minuend.coordinates[dimension] - self.coordinates[dimension] for dimension in range(dimensions)])

  # self-=subtrahend
  def __isub__(self, subtrahend):
    if not isinstance(subtrahend, Vertex):
      raise TypeError("Expected 'subtrahend' to be an instance of Vertex!")
    for dimension in range(min(len(self.coordinates), len(subtrahend.coordinates))):
      self.coordinates[dimension] -= subtrahend.coordinates[dimension]
    return self

  # ================================
  # Scaling Operations
  # ================================

  # self*multiplier
  def __mul__(self, multiplier):
    if not isinstance(multiplier, (int, float)):
      raise TypeError("Expected 'multiplier' to be a numerical type!")
    return Vertex(*[self.coordinates[dimension] * multiplier for dimension in range(len(self.coordinates))])

  # multiplicand*self
  def __rmul__(self, multiplicand):
    if not isinstance(multiplicand, (int, float)):
      raise TypeError("Expected 'multiplicand' to be a numerical type!")
    return Vertex(*[multiplicand * self.coordinates[dimension] for dimension in range(len(self.coordinates))])

  # self*=multiplier
  def __imul__(self, multiplier):
    if not isinstance(multiplier, (int, float)):
      raise TypeError("Expected 'multiplier' to be a numerical type!")
    for dimension in range(len(self.coordinates)):
      self.coordinates[dimension] *= multiplier
    return self

  # self/divisor
  def __truediv__(self, divisor):
    if not isinstance(divisor, (int, float)):
      raise TypeError("Expected 'divisor' to be a numerical type!")
    return Vertex(*[self.coordinates[dimension] / divisor for dimension in range(len(self.coordinates))])

  # self//divisor
  def __floordiv__(self, divisor):
    if not isinstance(divisor, (int, float)):
      raise TypeError("Expected 'divisor' to be a numerical type!")
    return Vertex(*[self.coordinates[dimension] // divisor for dimension in range(len(self.coordinates))])

  # dividend/self
  def __rdiv__(self, dividend):
    if not isinstance(dividend, (int, float)):
      raise TypeError("Expected 'dividend' to be a numerical type!")
    return Vertex(*[dividend / self.coordinates[dimension] for dimension in range(len(self.coordinates))])

  # self/=divisor
  def __idiv__(self, divisor):
    if not isinstance(divisor, (int, float)):
      raise TypeError("Expected 'divisor' to be a numerical type!")
    for dimension in range(len(self.coordinates)):
      self.coordinates[dimension] /= divisor
    return self


class Vertex2(Vertex):
  X = 0
  Y = 1

  def __init__(self, x, y):
    Vertex.__init__(self, x, y)

  @property
  def x(self):
    return self.coordinates[Vertex2.X]

  @x.setter
  def x(self, value):
    self.coordinates[Vertex2.X] = value

  @property
  def y(self):
    return self.coordinates[Vertex2.Y]

  @y.setter
  def y(self, value):
    self.coordinates[Vertex2.Y] = value

  def copy(self):
    return Vertex2(*self.coordinates)

  # self+addend
  def __add__(self, addend):
    return Vertex2(*Vertex.__add__(self, addend).coordinates)

  # augend+self
  def __radd__(self, augend):
    return Vertex2(*Vertex.__radd__(self, augend).coordinates)

  # self+=addend
  def __iadd__(self, addend):
    # TODO: Make this return self instead.
    return Vertex2(*Vertex.__iadd__(self, addend).coordinates)

  # self-subtrahend
  def __sub__(self, subtrahend):
    return Vertex2(*Vertex.__sub__(self, subtrahend).coordinates)

  # minuend-self
  def __rsub__(self, minuend):
    return Vertex2(*Vertex.__rsub__(self, minuend).coordinates)

  # self-=subtrahend
  def __isub__(self, subtrahend):
    # TODO: Make this return self instead.
    return Vertex2(*Vertex.__isub__(self, subtrahend).coordinates)

  # self*multiplier
  def __mul__(self, multiplier):
    return Vertex2(*Vertex.__mul__(self, multiplier).coordinates)

  # multiplicand*self
  def __rmul__(self, multiplicand):
    return Vertex2(*Vertex.__rmul__(self, multiplicand).coordinates)

  # self-=multiplier
  def __imul__(self, multiplier):
    Vertex.__imul__(self, multiplier)
    return self

  # self/divisor
  def __truediv__(self, divisor):
    return Vertex2(*Vertex.__truediv__(self, divisor).coordinates)

  # self//divisor
  def __floordiv__(self, divisor):
    return Vertex2(*Vertex.__floordiv__(self, divisor).coordinates)

  # dividend/self
  def __rdiv__(self, dividend):
    return Vertex2(*Vertex.__rdiv__(self, dividend).coordinates)

  # self/=divisor
  def __idiv__(self, divisor):
    Vertex.__idiv__(self, divisor)
    return self
    # return Vertex2(*Vertex.__idiv__(self, divisor).coordinates)
    # if not isinstance(divisor, (int, float)):
    #   raise TypeError("Expected 'divisor' to be a numerical type!")
    # for dimension in range(len(self.coordinates)):
    #   self.coordinates[dimension] *= divisor
    # return self


# Just a bit of testing :)
# TODO: Convert to unit tests.
if __name__ == "__main__":
  unit = 1
  print(f"Directional between (0, 0) and ({unit}, 0): {(Vertex2(0, 0) - Vertex2(unit, 0)).coordinates}")
  print(f"Directional between (0, 0) and ({unit}, {unit}): {(Vertex2(0, 0) - Vertex2(unit, unit)).coordinates}")
  print(f"Directional between (0, 0) and (0, {unit}): {(Vertex2(0, 0) - Vertex2(0, unit)).coordinates}")
  print(f"Directional between (0, 0) and (-{unit}, {unit}): {(Vertex2(0, 0) - Vertex2(-unit, unit)).coordinates}")
  print(f"Directional between (0, 0) and (-{unit}, 0): {(Vertex2(0, 0) - Vertex2(-unit, 0)).coordinates}")
  print(f"Directional between (0, 0) and (-{unit}, -{unit}): {(Vertex2(0, 0) - Vertex2(-unit, -unit)).coordinates}")
  print(f"Directional between (0, 0) and (0, -{unit}): {(Vertex2(0, 0) - Vertex2(0, -unit)).coordinates}")
  print(f"Directional between (0, 0) and ({unit}, -{unit}): {(Vertex2(0, 0) - Vertex2(unit, -unit)).coordinates}")

  multiplier = 3
  print(f"Multiplying ({unit}, 0) by {multiplier}: {(Vertex2(unit, 0) * multiplier).coordinates}")
  print(f"Multiplying ({unit}, {unit}) by {multiplier}: {(Vertex2(unit, unit) * multiplier).coordinates}")
  print(f"Multiplying (0, {unit}) by {multiplier}: {(Vertex2(0, unit) * multiplier).coordinates}")
  print(f"Multiplying (-{unit}, {unit}) by {multiplier}: {(Vertex2(-unit, unit) * multiplier).coordinates}")
  print(f"Multiplying (-{unit}, 0) by {multiplier}: {(Vertex2(-unit, 0) * multiplier).coordinates}")
  print(f"Multiplying (-{unit}, -{unit}) by {multiplier}: {(Vertex2(-unit, -unit) * multiplier).coordinates}")
  print(f"Multiplying (0, -{unit}) by {multiplier}: {(Vertex2(0, -unit) * multiplier).coordinates}")
  print(f"Multiplying ({unit}, -{unit}) by {multiplier}: {(Vertex2(unit, -unit) * multiplier).coordinates}")

  inline = Vertex2(1, 2)
  print(f"Pre inline mutliplication: {inline.coordinates}")
  for _ in range(multiplier):
    inline *= multiplier
    print(f"Multiplied ({inline.x}, {inline.y}) by {multiplier}: {inline.coordinates}")
  print(f"Post inline mutliplication: {inline.coordinates}")

