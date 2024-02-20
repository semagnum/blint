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


"""Runs BLint on one or multiple blend files, applying fixes if desired.

If a file is provided, will BLint just this file.
If a folder, BLint will iterate over all blend files within folder recursively.

Usage: ``offline_blinter.py [-h] [--fix] <blender> <path>``

- blender: path to Blender executable.
- path: filepath. file or folder to lint

"""

import sys
import os
import argparse


def collect_blend_files(curr_dir: str) -> list[str]:
    """Returns all blend files in a folder.

    :param curr_dir: root directory to begin search for blend files.
    """
    return [os.path.join(root, file)
            for root, dirs, files in os.walk(curr_dir)
            for file in files
            if file.endswith('.blend')]


def validate_args(validated_blender_path: str, validated_blend_path: str):
    """Validates Blender executable and blend filepaths.

    :param validated_blender_path: path to Blender executable.
    :param validated_blend_path: path to blend file.

    :raise FileNotFoundError: unable to find Blender executable or blend file.
    """
    if not validated_blender_path.endswith('.exe') or not os.path.exists(validated_blender_path) or not os.path.isfile(
            validated_blender_path):
        raise FileNotFoundError('Invalid blender executable filepath: {}'.format(validated_blender_path))

    if not os.path.exists(validated_blend_path):
        raise FileNotFoundError('Invalid blend path, use a directory or file: {}'.format(validated_blend_path))


def analyze_files(blender_path: str, blend_path: str, final_blend_files: list[str], auto_fix: bool = False):
    """Lints each blend file.

    :param final_blend_files: list of blend files to lint.
    :param auto_fix: if true, will apply any fixes available for rules.
    """
    import subprocess

    file_lint_checker_name = os.path.join(os.path.dirname(__file__), 'blinter_file_checker.py')

    for blend_file in final_blend_files:
        relpath = os.path.relpath(blend_file, start=blend_path)
        if relpath == '.':
            relpath = os.path.relpath(blend_file, start=os.path.dirname(blend_file))
        print('Linting {}...'.format(relpath if relpath != '.' else blend_file))
        program_args = [blender_path, blend_file, '-b', '-P', file_lint_checker_name]
        if auto_fix:
            program_args.extend(['--', '--blint-fix'])
        blend_app = subprocess.Popen(program_args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        log_prefix = 'blinter'
        prefix_len = len(log_prefix)
        for line in blend_app.stdout:
            if isinstance(line, bytes):
                line = line.decode('utf-8')
            if line.lstrip().find(log_prefix) == 0:
                sys.stdout.write(line.lstrip()[prefix_len:])
                sys.stdout.flush()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Runs blint on one or more blend files')
    parser.add_argument('blender', help='File location of the Blender\'s executable file')
    parser.add_argument('path', help='Path to blend file or folder containing blend files')
    parser.add_argument('--fix', '-f', action='store_true', help='Will automatically fix issues')

    args = parser.parse_args()

    try:
        validate_args(args.blender, args.path)
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)

    blend_path = str(args.path)
    # check if blender_path is a valid file
    blender_path = os.path.join(str(args.blender))

    blend_files = []
    if os.path.isdir(blend_path):
        print('Collecting blend files from directory: {}'.format(blend_path))
        blend_files = collect_blend_files(os.path.join(blend_path))
        if len(blend_files) == 0:
            print('No .blend files found in {}'.format(blend_path))
            sys.exit()
        print('Found {} .blend file(s)'.format(len(blend_files)))
    elif os.path.isfile(blend_path):
        print('Running linter on single file: {}'.format(blend_path))
        blend_files = [blend_path]
    else:
        print('Invalid blend path: {}'.format(blend_path))
        sys.exit()

    analyze_files(blender_path, blend_path, blend_files, args.fix)
