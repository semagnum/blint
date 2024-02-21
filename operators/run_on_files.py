import os
from threading import Thread

import bpy

from ..offline.offline_blinter import analyze_files, collect_blend_files, validate_args

START_BLINT_PRINT = ('-' * 16) + 'BLint Running' + ('-' * 16)


class BT_OT_RunOnFiles(bpy.types.Operator):
    """Creates new rule from the rule creation form in the preferences.

    External JSON file required to save new rule."""
    bl_idname = 'blint.run_on_files'
    bl_label = 'Run BLint on files'
    bl_description = 'Runs BLint checks on file or files, optionally including fixes'
    bl_options = {'REGISTER'}

    path: bpy.props.StringProperty(name='Path', subtype='FILE_PATH')
    fix: bpy.props.BoolProperty(
        name='Fix',
        description='Runs fixes for all rules that have them',
        default=False,
    )

    def validate(self, blender_path, blend_path):
        is_valid = True
        try:
            validate_args(blender_path, self.path)
        except FileNotFoundError as e:
            is_valid = False
            self.report({'ERROR'}, str(e))

        blend_files = []

        if os.path.isdir(blend_path):
            blend_files = collect_blend_files(str(os.path.join(blend_path)))
            if len(blend_files) == 0:
                self.report({'ERROR'}, 'No .blend files found in {}'.format(blend_path))
                is_valid = False
            else:
                self.report({'INFO'}, 'Found {} .blend file(s)'.format(len(blend_files)))
        elif os.path.isfile(blend_path):
            blend_files = [blend_path]
        else:
            self.report({'ERROR_INVALID_INPUT'}, 'Invalid blend path: {}'.format(blend_path))
            is_valid = False

        return is_valid, blend_files

    def modal(self, context, event):
        modal_status = 'PASS_THROUGH'

        if self._is_thread_done:
            context.window_manager.blint_running_progress = -1.0
            self.report({'INFO'}, 'BLint finished running, see system console for logs')
            modal_status = 'FINISHED'

        return {modal_status}

    def invoke(self, context, _event):
        blender_path = bpy.app.binary_path
        blend_path = bpy.path.abspath(self.path)

        is_valid, blend_files = self.validate(blender_path, blend_path)

        if not is_valid:
            return {'CANCELLED'}

        context.window_manager.blint_running_progress = 0.0

        self._is_thread_done = False
        self._curr_idx = 0
        self._total_files = len(blend_files)
        self._thread = Thread(
            target=analyze_files,
            args=(blender_path, blend_path, blend_files, self.fix, self.thread_callback)
        )

        print(START_BLINT_PRINT)
        self._thread.start()
        context.window_manager.modal_handler_add(self)

        return {'RUNNING_MODAL'}

    def thread_callback(self):
        wm = bpy.context.window_manager
        self._curr_idx += 1
        if self._curr_idx == self._total_files:
            self._is_thread_done = True
        wm.blint_running_progress = self._curr_idx / float(self._total_files)

    def execute(self, _context):
        blender_path = bpy.app.binary_path
        blend_path = bpy.path.abspath(self.path)

        is_valid, blend_files = self.validate(blender_path, blend_path)

        if not is_valid:
            return {'CANCELLED'}

        print(START_BLINT_PRINT)
        analyze_files(blender_path, blend_path, blend_files, self.fix)

        return {'FINISHED'}