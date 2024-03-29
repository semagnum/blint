# Copyright (C) 2023 Spencer Magnusson
# semagnum@gmail.com
# Created by Spencer Magnusson
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.


"""
Utility functions and data for retrieving and displaying icons.
"""

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
"""Accepted severity icons for rules, in the order of priority."""


def format_icon_name(icon: str) -> str:
    """Generates and returns icon's display name.

    :param icon: bpy icon data.
    """
    return icon.replace('_', ' ').title()


def get_icon_enum() -> list[tuple]:
    """Generates a ``bpy.props.EnumProperty`` set of items from get_icons()."""
    return [(icon, format_icon_name(icon), format_icon_name(icon), icon, idx)
            for idx, icon
            in enumerate(get_icons())
            ]


def get_icons() -> list[str]:
    """Retrieves a filtered list of all Blender icons, filtering excluded icon prefixes."""
    return [icon
            for icon
            in bpy.types.UILayout.bl_rna.functions["prop"].parameters["icon"].enum_items.keys()
            if icon != 'NONE' and
            icon not in severity_icons and
            not any((icon.startswith(prefix)
                     for prefix in excluded_icon_prefixes))
            and 'ARROW' not in icon
            ]


def get_severity_enum() -> list[tuple]:
    """Generates a ``bpy.props.EnumProperty`` set of items for all severity icons."""
    return [(icon, icon.title(), icon.title(), icon, idx)
            for idx, icon in enumerate(severity_icons)]


def bpy_data_enum() -> list[tuple]:
    """Generates a ``bpy.props.EnumProperty`` set of items for all icons representing bpy data types."""
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
