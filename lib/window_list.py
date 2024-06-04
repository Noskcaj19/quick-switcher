from typing import List
from PyQt6 import QtCore
from dataclasses import dataclass


@dataclass
class Window:
    id: str
    caption: str
    resource_class: str
    resource_name: str
    desktop_file: str


class Communicate(QtCore.QObject):
    changed = QtCore.pyqtSignal()


class WindowList:
    """
    A class to track windows ordered by most recently activated
    """

    # store all windows indexed by uuid
    windows: dict[str, Window] = {}
    # uuids in order of most recently accessed
    order: list[str] = []

    signals = Communicate()

    def add_window(self, window: Window):
        """
        adds a newly created window to the front of the list
        """
        self.windows[window.id] = window
        # add to order list, but only if it's not already there (avoid duplicates)
        if window.id not in self.order:
            self.order.insert(0, window.id)
        self.signals.changed.emit()

    def remove_window(self, id: str):
        if self.windows.pop(id, None) is not None:
            self.order.remove(id)
            self.signals.changed.emit()

    def mark_activated(self, window: Window):
        # move window to front of order list
        self.add_window(window)
        self.order.pop(self.order.index(window.id))
        self.order.insert(0, window.id)
        self.signals.changed.emit()

    def update_caption(self, window: Window):
        self.add_window(window)
        self.windows[window.id].caption = window.caption
        self.signals.changed.emit()

    def ordered_windows(self) -> List[Window]:
        out = []
        for i in self.order:
            window = self.windows.get(i)
            if window is None:
                continue
            if window.caption == "KcajSwitcher":
                continue
            out.append(window)
        return out

    def __str__(self) -> str:
        out = ""
        for id in self.order:
            out += f"{id} {self.windows[id].caption}\n"
        return out
