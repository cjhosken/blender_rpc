import bpy
from bpy.types import AddonPreferences
from bpy.props import BoolProperty, StringProperty

class BlenderRichPresence_Preferences(AddonPreferences):
    bl_idname = __package__

    hide_details: BoolProperty(
        name = "Hide Details",
        description= "Hide extra info about your project",
        default=False
    )

    client_id : StringProperty(
        name = "Client ID",
        default = "363326394987708417",
    )

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop(self, "client_id")
        row.prop(self, "hide_details")
        row = layout.row()()
        row.operator("wm.url_open", text="Report Bug", icon="URL").url = "https://github.com/Christopher-Hosken/blender_rpc/issues"


def get_user_preferences(context=None):
    if not context:
        context = bpy.context

    if hasattr(context, "user_preferences"):
        prefs = context.user_preferences.addons.get(__package__, None)
    elif hasattr(context, "preferences"):
        prefs = context.preferences.addons.get(__package__, None)
    if prefs:
        return prefs.preferences
    return None

classes = [BlenderRichPresence_Preferences]