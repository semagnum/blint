import sys
import os
import argparse
parser = argparse.ArgumentParser(description='Runs blint on one or more blend files')
parser.add_argument('blender', help='File location of the Blender\'s executable file')
parser.add_argument('path', help='Path to blend file or folder containing blend files')
parser.add_argument('--fix', '-f', action='store_true', help='Will automatically fix issues')

args = parser.parse_args()

file_lint_checker_name = os.path.join(os.path.dirname(__file__), 'blinter_file_checker.py')


def collect_blend_files(curr_dir):
    return [os.path.join(root, file)
            for root, dirs, files in os.walk(curr_dir)
            for file in files
            if file.endswith('.blend')]


def validate_args(validated_blender_path, validated_blend_path):
    if not validated_blender_path.endswith('.exe') or not os.path.exists(validated_blender_path) or not os.path.isfile(
            validated_blender_path):
        raise FileNotFoundError('Invalid blender executable filepath: {}'.format(validated_blender_path))

    if not os.path.exists(validated_blend_path):
        raise FileNotFoundError('Invalid blend path, use a directory or file: {}'.format(validated_blend_path))

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


def analyze_files(final_blend_files, auto_fix=False):
    import subprocess

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
            if type(line) == bytes:
                line = line.decode('utf-8')
            if line.lstrip().find(log_prefix) == 0:
                sys.stdout.write(line.lstrip()[prefix_len:])
                sys.stdout.flush()

analyze_files(blend_files, args.fix)
