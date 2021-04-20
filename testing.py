

from measurements import Measurement
from units.time import Seconds
from units.prefixes.large import Kilo
from units.prefixes.small import Milli


seconds = Measurement(1.2, Seconds())
print(f"seconds: {seconds}")

milliseconds = seconds.convertTo(Milli())
print(f"{seconds} = {milliseconds}")
seconds = milliseconds.inBaseUnits()
print(f"{milliseconds} = {seconds}")

kiloseconds = seconds.convertTo(Kilo())
print(f"{seconds} = {kiloseconds}")
seconds = kiloseconds.inBaseUnits()
print(f"{kiloseconds} = {seconds}")

milliseconds = kiloseconds.convertTo(Milli())
print(f"{kiloseconds} = {milliseconds}")

kiloseconds = milliseconds.convertTo(Kilo())
print(f"{milliseconds} = {kiloseconds}")

