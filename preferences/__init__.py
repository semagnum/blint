import bpy

from . import preferences


def register():
    bpy.utils.register_class(preferences.BT_MT_config_menu)
    bpy.utils.register_class(preferences.SA_Preferences)


def unregister():
    bpy.utils.unregister_class(preferences.SA_Preferences)
    bpy.utils.unregister_class(preferences.BT_MT_config_menu)
