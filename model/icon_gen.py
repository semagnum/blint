import bpy

excluded_icon_prefixes = ('BRUSH_', 'MATCAP_', 'EVENT_', 'MOUSE_', 'COLORSET_', 'ZOOM_',
                          'TRIA_', 'DISCLOSURE_', 'GPBRUSH_', 'TRACKING_', 'KEYTYPE_', 'HANDLETYPE_',
                          'COLLECTION_COLOR_', 'SEQUENCE_COLOR_')

allowed_bpy_data = ['actions', 'armatures', 'brushes', 'cache_files', 'cameras', 'collections', 'curves', 'fonts',
                    'grease_pencils', 'images', 'lattices', 'libraries', 'lightprobes', 'lights', 'linestyles',
                    'masks', 'materials', 'meshes', 'metaballs', 'movieclips', 'node_groups', 'objects',
                    'paint_curves', 'palettes', 'particles', 'pointclouds', 'scenes', 'screens', 'shape_keys',
                    'sounds', 'speakers', 'texts', 'textures', 'volumes', 'window_managers', 'workspaces', 'worlds']

severity_icons = ['ERROR', 'INFO']


def format_icon_name(icon):
    return icon.replace('_', ' ').title()


def get_icon_enum():
    return [(icon, format_icon_name(icon), format_icon_name(icon), icon, idx)
            for idx, icon
            in enumerate(get_icons())
            ]


def get_icons():
    return [icon
            for icon
            in bpy.types.UILayout.bl_rna.functions["prop"].parameters["icon"].enum_items.keys()
            if icon != 'NONE' and
            icon not in severity_icons and
            not any((icon.startswith(prefix)
                     for prefix in excluded_icon_prefixes))
            and 'ARROW' not in icon
            ]


def get_severity_enum():
    return [(icon, icon.title(), icon.title(), icon, idx)
            for idx, icon in enumerate(severity_icons)]


def bpy_data_enum():
    icons = get_icons()
    data_icons = [i for i in icons if 'DATA' in i]
    data_to_icon = {
        data: 'SCENE_DATA'
        for data in allowed_bpy_data
    }
    # lowest priority: any matching icon
    data_to_icon.update({
        data: icon
        for data in allowed_bpy_data
        for icon in icons
        if data[:-1].lower() in icon.lower() or data.lower() in icon.lower()
    })
    # next priority: any matching data icon
    data_to_icon.update({
        data: icon
        for data in allowed_bpy_data
        for icon in data_icons
        if data[:-1].lower() in icon.lower() or data.lower() in icon.lower()
    })
    # top priority: any matching icon starting with term
    data_to_icon.update({
        data: icon
        for data in allowed_bpy_data
        for icon in data_icons
        if icon.lower().startswith(data[:-1].lower())
    })
    return [
        (data, format_icon_name(data), data, data_to_icon[data], idx)
        for idx, data
        in enumerate(allowed_bpy_data)
    ]