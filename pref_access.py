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


from .config import PACKAGE_NAME


def get_user_preferences(context):
    """Returns BLint preferences and attributes.

    :param context: Blender's context
    """
    if hasattr(context, "user_preferences"):
        return context.user_preferences.addons[PACKAGE_NAME].preferences

    return context.preferences.addons[PACKAGE_NAME].preferences
