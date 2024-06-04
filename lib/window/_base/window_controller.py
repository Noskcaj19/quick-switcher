from typing import List

from lib.window_list import Window


class WindowController:
    def get_updated_signal(self):
        raise NotImplementedError()

    def start(self):
        raise NotImplementedError()

    def stop(self):
        raise NotImplementedError()

    def activate_window(self, window_id: str):
        raise NotImplementedError()

    def windows(self) -> List[Window]:
        raise NotImplementedError()
