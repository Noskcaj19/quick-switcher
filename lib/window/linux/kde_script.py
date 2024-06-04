import os

from .dbus import SwitcherListener


class KdeScript:
    id = None

    def __init__(self, bus) -> None:
        # self.scripting = bus.get("org.kde.KWin", "/Scripting")["org.kde.kwin.Scripting"]
        self.bus = bus
        scripting_introspection = bus.introspect_sync("org.kde.KWin", "/Scripting")

        proxy_object = bus.get_proxy_object(
            "org.kde.KWin", "/Scripting", scripting_introspection
        )
        self.scripting = proxy_object.get_interface("org.kde.kwin.Scripting")

    def load_script(self, path: str):
        # self.id = self.scripting.loadScript(os.path.abspath(path))
        self.id = self.scripting.call_load_script_sync(os.path.abspath(path))
        print("loaded script ", self.id)

    def run(self):
        assert self.id is not None
        script_introspection = self.bus.introspect_sync(
            "org.kde.KWin", f"/Scripting/Script{self.id}"
        )
        proxy_object = self.bus.get_proxy_object(
            "org.kde.KWin", f"/Scripting/Script{self.id}", script_introspection
        )
        self.script_object = proxy_object.get_interface("org.kde.kwin.Script")
        self.script_object.call_run_sync()
        # script = bus.get("org.kde.KWin", f"/Scripting/Script{self.id}")["org.kde.kwin.Script"]
        # script.run()

    def stop(self):
        assert self.id is not None
        # script = bus.get("org.kde.KWin", f"/Scripting/Script{self.id}")["org.kde.kwin.Script"]
        self.script_object.call_stop_sync()
        self.id = None
