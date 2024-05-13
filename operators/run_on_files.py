import os
import logging
from threading import Thread
import subprocess
import sys

import bpy

from ..offline import offline_blinter

START_BLINT_PRINT = ('-' * 16) + 'BLint Running' + ('-' * 16)
log = logging.getLogger(__name__)


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
            offline_blinter.validate_args(blender_path, self.path)
        except FileNotFoundError as e:
            is_valid = False
            self.report({'ERROR'}, str(e))

        blend_files = []

        if os.path.isdir(blend_path):
            blend_files = offline_blinter.collect_blend_files(str(os.path.join(blend_path)))
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
            self.report({'INFO'}, 'BLint finished, see system console')
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
            target=self.analyze,
            args=(context.window_manager, blender_path, blend_files)
        )

        self._thread.start()
        context.window_manager.modal_handler_add(self)

        return {'RUNNING_MODAL'}

    def analyze(self, window_manager, blender_path, blend_files):
        python_path = bpy.path.abspath(sys.executable)
        offline_blinter_path = os.path.abspath(offline_blinter.__file__)

        for file in blend_files:
            args = [
                python_path,
                offline_blinter_path,
                blender_path,
                file
            ] + (['--fix'] if self.fix else [])

            try:
                blend_app = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                for line in blend_app.stdout:
                    if isinstance(line, bytes):
                        line = line.decode('utf-8').strip()

                    log.warning(line)
            except subprocess.CalledProcessError as e:
                log.error(str(e))

            self._curr_idx += 1
            window_manager.blint_running_progress = self._curr_idx / float(self._total_files)

        self._is_thread_done = True

    def execute(self, context):
        blender_path = bpy.app.binary_path
        blend_path = bpy.path.abspath(self.path)

        is_valid, blend_files = self.validate(blender_path, blend_path)

        if not is_valid:
            return {'CANCELLED'}

        self.analyze(context.window_manager, blender_path, blend_files)

        return {'FINISHED'}