import sys
from PyQt6.QtWidgets import QApplication

from .ui import MainWindow
from .window.window_controller import WindowController

app = QApplication(sys.argv)

window_controller = WindowController()
window_controller.start()

window = MainWindow(window_controller)
window.show()


def exiting():
    print("exiting")
    window_controller.stop()
    print("script stopped")


import atexit

atexit.register(exiting)

app.exec()
