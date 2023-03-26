from threading import Thread

from ..preferences import get_user_preferences
from ..pypresence.pypresence import Presence
from ..pypresence.pypresence import exceptions
from .BlenderProject import BlenderProject



class BlenderPresence(Thread):
    _client = None
    _blender_project = None
    _stopped = None
    _event = None

    _state = None
    _details = None
    _largeIcon = "blender"

    def __init__(self, event) -> None:
        super().__init__()
        self._blender_project = BlenderProject()
        self._client = Presence(get_user_preferences().client_id)
        self._stopped = event

    def start(self) -> None:
        self._blender_project._connected = self.connect()
        return super().start()

    def connect(self):
        try: 
            self._client.connect()
            print("Discord: Blender Connected.")
            return True
        except ConnectionRefusedError:
            print("Discord: Connection Refused.")
            return False
        except (FileNotFoundError, AttributeError, exceptions.InvalidPipe, AssertionError):
            print("Discord: Client not found.")
            return False

    def run(self) -> None:
        while not self._stopped.wait(0.5):
                self.update_presence()

    def update_presence(self):
        prefs = get_user_preferences()

        name = f"Workspace: {self._blender_project.get_file_name()}"
        start = self._blender_project.get_start()
        info = "  "

        if (not prefs.hide_details):
            if (self._blender_project._is_rendering):
                info += "Rendering frame " + self._blender_project.get_current_frame() + self._blender_project.get_render_engine()
            else:
                info += "Editing " + '"' + self._blender_project.get_active_object() + '"'  + " in " + self._blender_project.get_current_mode()
            
        if (self._blender_project._connected):
            try:
                self._client.update(
                    state=name,
                    details=info,
                    start=start,
                    large_text=self._blender_project.get_blender_version(),
                    large_image="blender"
                )
            except exceptions.InvalidID or AssertionError:
                self._blender_project._connected = False
                print("Discord: Lost connection to Blender. Reconnecting...")
                self._blender_project._connected = self.connect()
        else:
            print("Discord: Reconnecting...")
            self._blender_project._connected = self.connect()
    
    def stop(self):
        self._blender_project._connected = False
        if (self._blender_project._connected):
            self._client.clear()
        self._stopped.set()
            
    

