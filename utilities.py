

def escapes(lower, coordinate, velocity, upper):
  """
  Determines if the projected coordinate by the velocity escapes a defined lower or upper boundary.

  Returns one of the following values:
    * Negative: The projected coordinate escaped the lower boundary by the returned amount.
    * Neutral: The projected coordinate stayed within both the lower and upper boundary.
    * Positive: The projected coordinate escaped the upper boundary by the returned amount.
  """
  result = 0 # Assume the projected coordinate stays within both the lower and upper boundary.

  if coordinate + velocity < lower:
    result = lower - (coordinate - velocity)
  elif upper < coordinate + velocity:
    result = (coordinate + velocity) - upper

  return result


def reflect(lower, current, modifier, upper):
  """
  Reflects a projected position if it escapes the bounds.
  """
  next, modified = current, modifier

  if next + modified < lower:
    modified *= -1
    next = lower + (modified - next + lower)
  elif upper < next + modified:
    next = upper - (next + modified - upper)
    modified *= -1
  else:
    next += modified

  # escaped = escapes(lower, current, modifier, upper)

  # if escaped < 0:
  #   next = lower - escaped
  #   modified *= -1
  # elif 0 < escaped:
  #   next = upper - escaped
  #   modified *= -1
  # else:
  #   next += modified

  return (next, modified)


if __name__ == "__main__":
  print(f"escapes(0, 1, -5, 20)? {escapes(0, 1, -5, 20)}")
  print(f"escapes(0, 4, 5, 20)? {escapes(0, 4, 5, 20)}")
  print(f"escapes(0, 19, 5, 20)? {escapes(0, 19, 5, 20)}")
  print(f"escapes(0, 16, -5, 20)? {escapes(0, 16, -5, 20)}")

