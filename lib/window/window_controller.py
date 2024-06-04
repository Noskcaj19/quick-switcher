import os
import sys


if sys.platform == "linux":
    from .linux.window_controller import WindowController
elif sys.platform == "win32":
    from .windows.window_controller import WindowController
else:
    pass
