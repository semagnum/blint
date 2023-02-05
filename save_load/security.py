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


def security_check(expression: str):
    """Checks if there is insecure code, specifically ``eval()`` and ``exec()``, otherwise returns nothing.

    :param expression: Python code in the form of a string.

    :raise ValueError: if expression contains insecure code.

    """
    if 'eval(' in expression or 'exec(' in expression:
        raise ValueError('Expression contains insecure code: {}'.format(expression))
