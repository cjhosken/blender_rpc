#
#    Copyright (C) 2023 Christopher Hosken
#    hoskenchristopher@gmail.com
#
#    Created by Christopher Hosken
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

__copyright__ = "(c) 2023, Christopher Hosken"
__license__ = "GPL v3"

bl_info = {
    "name" : "Blender Rich Presence",
    "author" : "Christopher Hosken",
    "description" : "",
    "blender" : (3, 4, 0),
    "version" : (1, 0, 0),
    "category" : "System"
}

from threading import Event
from time import time

from .blenderpresence.BlenderPresence import BlenderPresence
from . import auto_load
from .preferences import classes as preferences_classes

from bpy.app.handlers import render_init, render_complete, render_cancel, render_post, load_post, persistent

classes = []
classes += preferences_classes

auto_load.init()

STOP_FLAG = Event()

presence = None

@persistent
def start_render_job_handler(arg):
    presence._blender_project._is_rendering = True

@persistent
def end_render_job_handler(arg):
    presence._blender_project._is_rendering = False
    presence._blender_project._rendered_frames = 0

@persistent   
def post_render_handler(arg):
    presence._blender_project._rendered_frames += 1

@persistent
def load_post_handler(arg):
    presence._blender_project._start = time()

handlers = [
    (render_init, start_render_job_handler), 
    (render_complete, end_render_job_handler), 
    (render_cancel, end_render_job_handler), 
    (render_post, post_render_handler), 
    (load_post, load_post_handler)
]

def start_presence():
    presence.start()

def register():
    global presence

    import bpy
    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)

    presence = BlenderPresence(STOP_FLAG)

    bpy.app.timers.register(start_presence, first_interval=5, persistent=True)

    for handle in handlers:
        handle[0].append(handle[1])

    bpy.context.preferences.use_preferences_save = True

    start_presence()

def unregister():
    import bpy
    from bpy.utils import unregister_class

    if (presence is not None and presence.is_alive()):
        presence.stop()
    
    if (bpy.app.timers.is_registered(start_presence)):
        bpy.app.timers.unregister(start_presence)
    
    for cls in reversed(classes):
        unregister_class(cls)

    for handle in handlers:
        if (handle[1] in handle[0]):
            handle[0].remove(handle[1])

if __name__ == "__main__":
    try:
        register()
    except ValueError:
        unregister()
        register()