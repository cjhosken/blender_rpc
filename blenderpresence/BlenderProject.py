from cgitb import reset
from enum import Enum
import bpy, time, os
from bpy.app.handlers import persistent

class BlenderProject:
    _start = None
    _connected = False
    _is_rendering = False
    _rendered_frames = 0

    def __init__(self):
        self._start = time.time()

    def get_start(self):
        return self._start

    def get_file_name(self):
        name = bpy.path.display_name_from_filepath(bpy.data.filepath)

        if (name == ""):
            name="untitled"

        name += ".blend"

        return name
    
    def get_blender_version(self):
        return str(bpy.app.version_string)

    def get_current_mode(self):
        if (bpy.context.view_layer.objects.active):
            active_mode = bpy.context.view_layer.objects.active.mode
            for i in MODES:
                if i in active_mode:
                    return str(MODES[i][0])
        else:
            return "Object Mode"
        

    def get_active_object(self):
        if (bpy.context.view_layer.objects.active):
            return str(bpy.context.view_layer.objects.active.name)
        else:
            return " "

    def get_current_frame(self):
        return str(bpy.context.scene.frame_current)

    def get_render_engine(self):
        engine = bpy.context.engine
        print(bpy.context.engine)
        for i in ENGINES:
                if i in engine:
                    return " in " + str(ENGINES[i][0])
        return " "
    
    def get_frame_range(self):
        start = str(bpy.context.scene.frame_start)
        end = str(bpy.context.scene.frame_end)
        return (start, end)

MODES = {
    "OBJECT" : ["Object Mode", "object"],
    "EDIT": ["Edit Mode", "edit"],
    "POSE": ["Pose Mode", "pose"],
    "SCULPT": ["Sculpt Mode", "sculpt"],
    "PAINT_GPENCIL": ["Draw Mode", "paint_gpencil"],
    "TEXTURE_PAINT": ["Texture Paint Mode", "texture_paint"],
    "VERTEX_PAINT": ["Vertex Paint Mode", "vertex_paint"],
    "WEIGHT_PAINT": ["Weight Paint Mode", "weight_paint"],
    "PARTICLE_EDIT": ["Particle Edit Mode", "particle_edit"],
}


ENGINES = {
    "CYCLES" : ["Cycles", "cycles"],
    "EEVEE" : ["Eevee", "eevee"],
    "BLENDER_WORKBENCH" :  ["Workbench", "workbench"]
}