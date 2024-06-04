from threading import Thread
import asyncio
from typing import List
from dbus_next.aio.message_bus import MessageBus as AIOMessageBus
from dbus_next.glib.message_bus import MessageBus as GIOMessageBus
from dbus_next.service import ServiceInterface, method, dbus_property, signal
from dbus_next.signature import Variant
from dbus_next.errors import DBusError

from lib.window_list import Window

from .kde_script import KdeScript

from .dbus import SwitcherListener
from .._base.window_controller import WindowController as BaseWindowController


class WindowController(BaseWindowController):
    switchener = SwitcherListener()

    def get_updated_signal(self):
        return self.switchener.window_list.signals.changed

    async def _async_job(self):
        bus = await AIOMessageBus().connect()
        bus.export("/com/noskcaj/Switcher", self.switchener)
        await bus.request_name("com.noskcaj.Switcher")
        await bus.wait_for_disconnect()

    def _loop_in_thread(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._async_job())

    def start(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        thread = Thread(target=self._loop_in_thread, args=(loop,), daemon=True)
        thread.start()

        bus = GIOMessageBus().connect_sync()

        self.script = KdeScript(bus)
        self.script.load_script("./lib/window/linux/plasma-script.js")
        self.script.run()

    def stop(self):
        assert self.script is not None
        self.script.stop()

    def activate_window(self, window_id: str):
        self.switchener.activate_window(window_id)

    def windows(self) -> List[Window]:
        return self.switchener.window_list.ordered_windows()
