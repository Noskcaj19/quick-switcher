import asyncio


class TSAsyncEvent(asyncio.Event):
    def set(self):
        self._loop.call_soon_threadsafe(super().set)  # type: ignore

    def clear(self):
        self._loop.call_soon_threadsafe(super().clear)  # type: ignore
