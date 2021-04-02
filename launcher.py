
from demos.painting import PaintingDemo as Demo
# from demos.emitter import EmittingDemo as Demo
# from demos.bouncer import BouncingDemo as Demo

WINDOW_LENGTH = 640
WINDOW_HEIGHT = 480
# WINDOW_LENGTH = 1280
# WINDOW_HEIGHT = 720

demo = Demo()
demo.run(WINDOW_LENGTH, WINDOW_HEIGHT, False)
del demo
