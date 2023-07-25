if 'bpy' in locals():
    import importlib

    reloadable_modules = [
        'preferences',
    ]
    for module_name in reloadable_modules:
        if module_name in locals():
            importlib.reload(locals()[module_name])

import bpy

from . import preferences


def register():
    bpy.utils.register_class(preferences.SA_Preferences)


def unregister():
    bpy.utils.unregister_class(preferences.SA_Preferences)
