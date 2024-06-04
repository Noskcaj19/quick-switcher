from typing import List
from PyQt6.QtGui import QKeyEvent
from PyQt6 import QtCore
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QMainWindow, QListView, QWidget, QVBoxLayout

from pfzy import fuzzy_match
import asyncio

from .window.window_controller import WindowController
from lib.window_list import WindowList, Window


def filter_windows(query: str, windows: List[Window]) -> List[Window]:
    if query.strip() == "":
        return windows
    else:
        return [
            i["window"]
            for i in asyncio.run(
                fuzzy_match(
                    query,
                    [
                        {"caption": window.caption, "window": window}
                        for window in windows
                    ],
                    key="caption",
                )
            )
        ]


class WindowListModel(QtCore.QAbstractListModel):
    window_controller: WindowController
    filter: str = ""
    filtered_windows: list[Window] = []

    def __init__(self, window_controller: WindowController, *args, **kwargs):
        super(WindowListModel, self).__init__(*args, **kwargs)
        self.window_controller = window_controller
        self.window_controller.get_updated_signal().connect(self.update_filted)
        self.update_filted()

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            # window = self.window_list[index.row()]
            window = self.filtered_windows[index.row()]
            if window is None:
                return "<none>"
            return window.resource_name + " | " + window.caption

    def update_filted(self):
        self.filtered_windows = filter_windows(
            self.filter, self.window_controller.windows()
        )
        self.layoutChanged.emit()

    def set_filter(self, filter: str):
        self.filter = filter
        self.update_filted()

    def rowCount(self, index):
        return len(self.filtered_windows)


class ForwardingQListView(QListView):
    def keyPressEvent(self, a0):
        a0.ignore()


class WindowListWidget(QWidget):
    filter = ""

    def __init__(self, window_controller: WindowController):
        super(WindowListWidget, self).__init__()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.window_list_view = ForwardingQListView()
        # window_list_view.setFixedSize(200, 200)
        self.model = WindowListModel(window_controller)
        self.window_controller = window_controller
        self.window_list_view.setModel(self.model)
        layout.addWidget(self.window_list_view)

        self.setLayout(layout)

    def keyPressEvent(self, a0: QKeyEvent | None) -> None:
        assert a0 is not None
        print("keypre", a0.text(), a0.key(), Qt.Key.Key_Return, self.filter)
        if a0.key() == Qt.Key.Key_Return:
            print("enter")
            index = self.window_list_view.selectedIndexes()[0]
            window = self.model.filtered_windows[index.row()]
            assert window is not None
            print("activating", window.caption)
            from threading import current_thread

            print(current_thread().native_id)
            self.window_controller.activate_window(window.id)

        if a0.text().isprintable():
            self.filter += a0.text()
        if a0.key() == Qt.Key.Key_Backspace:
            self.filter = self.filter[:-1]
        self.model.set_filter(self.filter)

        return super().keyPressEvent(a0)


class MainWindow(QMainWindow):
    window_list: WindowList

    def __init__(self, window_controller: WindowController):
        super().__init__()
        self.window_controller = window_controller
        self.setWindowTitle("KcajSwitcher")

        self.setFixedSize(QSize(400, 300))

        self.setCentralWidget(WindowListWidget(window_controller))

    # def closeEvent(self, event):
    #     event.accept()
