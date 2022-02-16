import bpy


class BT_OT_FixIssue(bpy.types.Operator):
    bl_idname = 'scene_analyzer.fix_issue'
    bl_label = 'Fix issue'
    bl_description = 'Fix issue'
    bl_options = {'REGISTER', 'UNDO'}

    fix: bpy.props.StringProperty(default='')

    def execute(self, context):
        print('Running:', self.fix)
        exec(self.fix)
        return {'FINISHED'}
