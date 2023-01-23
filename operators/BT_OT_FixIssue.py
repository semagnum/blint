import bpy


class BT_OT_FixIssue(bpy.types.Operator):
    """Runs a given BLint fix on the scene."""
    bl_idname = 'scene_analyzer.fix_issue'
    bl_label = 'Fix issue'
    bl_description = 'Fix issue'
    bl_options = {'REGISTER', 'UNDO'}

    fix: bpy.props.StringProperty(default='')
    """Python expression to fix issue in scene."""

    def execute(self, context):
        print('Running:', self.fix)
        exec(self.fix)
        return {'FINISHED'}
