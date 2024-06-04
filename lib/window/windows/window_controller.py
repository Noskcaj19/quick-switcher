from PyQt6 import QtCore
from typing import List

from lib.window_list import Window, WindowList
from .._base.window_controller import WindowController as BaseWindowController


class WindowController(BaseWindowController):
    window_list = WindowList()

    def get_updated_signal(self):
        return self.window_list.signals.changed

    def start(self):
        pass

    def stop(self):
        pass

    def activate_window(self, window_id: str):
        pass

    def windows(self) -> List[Window]:
        return [Window("invalid", "Demo", "Demo RC", "Demo RN", "")]
