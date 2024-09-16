"""Template file rule.

If you would like to test this rule, add it to your BLint config with the following:

{
    "description": "(script) Unapplied scale on modified object",
    "enabled": true,
    "rule_file": "C:\\PATH\\TO\\external_rule_template.py"
}

"""

import bpy
from mathutils import Matrix


def get_issue_objects():
    """Not required, just a convenience method to get the issue-related list of datablocks."""
    return [
        my_object
        for my_object in bpy.data.objects
        if tuple(my_object.scale) != (1.0, 1.0, 1.0) and any(m.type in {'BEVEL', 'SOLIDIFY'} for m in my_object.modifiers)
    ]


def get_issues():
    """Template function to retrieve and display issues.

    Returns:
        A list[dict] representing each issue, with each element as:
        {
            'description': 'A string used as the issue label',
            'severity_icon': 'str in ['ERROR', INFO']',
            'category_icon': 'Icon name found in Blender',
            'fix_expr': 'str (see below)'
        }

        The fix_expr can be:
            - empty, meaning no fix
            - Python code in str form, just like BLint's default usage of fix_expr
            - a unique argument to pass to fix_issues() to identify which issue to fix, in this case the object's name
    """
    return [
        {
            'description': my_object.name + ': unapplied scale on modified object',
            'severity_icon': 'INFO',
            'category_icon': 'MODIFIER',
            'fix_expr': my_object.name
        }
        for my_object in get_issue_objects()
    ]


def fix_issues(*args):
    """Template function to fix issues. If not provided, will default to the issue's own fix_expr.

    Passing a unique argument, like a datablock name, will prevent IndexErrors when running fixes one after the other.

    Args:
        *args: single element, a "key" to a given issue, in this case the object's name.

    """
    obj_name = args[0]
    if obj_name not in [obj.name for obj in get_issue_objects()]:
        return

    obj = bpy.data.objects[obj_name]
    mat = obj.matrix_local
    _, _, scale = mat.decompose()
    mat_scale = Matrix.LocRotScale(None, None, scale)
    obj.data.transform(mat_scale)
    obj.scale = 1, 1, 1