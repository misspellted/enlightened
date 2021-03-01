
#from demos.painting import PaintingDemo as Demo
from demos.emitter import EmittingDemo as Demo

WINDOW_LENGTH = 640
WINDOW_HEIGHT = 480

demo = Demo()
demo.run(WINDOW_LENGTH, WINDOW_HEIGHT)
del demo
