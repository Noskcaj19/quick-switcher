from lib.window_list import *
from dbus_next.service import ServiceInterface, method
import asyncio

from .TSAsyncEvent import TSAsyncEvent


class SwitcherListener(ServiceInterface):
    """
    <node>
            <interface name='com.noskcaj.Switcher'>
                    <method name='NotifyActiveWindow'>
                            <arg type='s' name='internal_id' direction='in'/>
                            <arg type='s' name='caption' direction='in'/>
                            <arg type='s' name='resource_class' direction='in'/>
                            <arg type='s' name='resource_name' direction='in'/>
                            <arg type='s' name='desktop_file' direction='in'/>
                    </method>
                    <method name='NotifyCaptionChanged'>
                            <arg type='s' name='internal_id' direction='in'/>
                            <arg type='s' name='caption' direction='in'/>
                            <arg type='s' name='resource_class' direction='in'/>
                            <arg type='s' name='resource_name' direction='in'/>
                            <arg type='s' name='desktop_file' direction='in'/>
                    </method>
                    <method name='NotifyAddedWindow'>
                            <arg type='s' name='internal_id' direction='in'/>
                            <arg type='s' name='caption' direction='in'/>
                            <arg type='s' name='resource_class' direction='in'/>
                            <arg type='s' name='resource_name' direction='in'/>
                            <arg type='s' name='desktop_file' direction='in'/>
                    </method>
                    <method name='NotifyRemovedWindow'>
                            <arg type='s' name='internal_id' direction='in'/>
                    </method>
                    <method name='PollActivate'>
                            <arg type='s' name='out' direction='out'/>
                    </method>
            </interface>
    </node>
    """

    def __init__(self):
        super().__init__("com.noskcaj.Switcher")

    window_list = WindowList()

    @method()
    def NotifyActiveWindow(self, id: "s", caption: "s", resource_class: "s", resource_name: "s", desktop_file: "s"):  # type: ignore
        self.window_list.mark_activated(
            Window(id, caption, resource_class, resource_name, desktop_file)
        )

    @method()
    def NotifyCaptionChanged(self, id: "s", caption: "s", resource_class: "s", resource_name: "s", desktop_file: "s"):  # type: ignore
        self.window_list.update_caption(
            Window(id, caption, resource_class, resource_name, desktop_file)
        )

    @method()
    def NotifyAddedWindow(self, id: "s", caption: "s", resource_class: "s", resource_name: "s", desktop_file: "s"):  # type: ignore
        self.window_list.add_window(
            Window(id, caption, resource_class, resource_name, desktop_file)
        )

    @method()
    def NotifyRemovedWindow(self, id: "s"):  # type: ignore
        self.window_list.remove_window(id)

    polling_event = TSAsyncEvent()
    activate_window_id = None

    @method()
    async def PollActivate(self) -> "s":  # type: ignore
        await self.polling_event.wait()
        self.polling_event.clear()
        win = self.activate_window_id
        self.activate_window_id = None
        return win

    def activate_window(self, id: str):
        self.activate_window_id = id
        self.polling_event.set()
