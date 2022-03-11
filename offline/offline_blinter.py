import sys
import os

file_lint_checker_name = os.path.join(os.path.dirname(__file__), 'blinter_file_checker.py')


def collect_blend_files(curr_dir):
    return [os.path.join(root, file)
            for root, dirs, files in os.walk(curr_dir)
            for file in files
            if file.endswith('.blend')]


def validate_args(args):
    if any('help' in x for x in args) or len(args) < 2:
        print(
            'Usage: python offline_linter.py [Blender.exe filepath] [directory of .blend files or a single .blend file]')
        sys.exit()

    validated_blend_path = str(args[2])

    # check if blender_path is a valid file
    validated_blender_path = os.path.join(str(args[1]))
    if not validated_blender_path.endswith('.exe') or not os.path.exists(validated_blender_path) or not os.path.isfile(
            validated_blender_path):
        print('Invalid blender path: {}'.format(validated_blender_path))
        sys.exit()

    if not os.path.exists(validated_blend_path):
        print('Invalid blend path, use a directory or file: {}'.format(validated_blend_path))
        sys.exit()


validate_args(sys.argv)

blend_path = str(sys.argv[2])
# check if blender_path is a valid file
blender_path = os.path.join(str(sys.argv[1]))

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


def analyze_files(final_blend_files):
    import subprocess

    for blend_file in final_blend_files:
        relpath = os.path.relpath(blend_file, start=blend_path)
        if relpath == '.':
            relpath = os.path.relpath(blend_file, start=os.path.dirname(blend_file))
        print('Linting {}...'.format(relpath if relpath != '.' else blend_file))
        program_args = [blender_path, blend_file, '-b', '-P', file_lint_checker_name]
        blend_app = subprocess.Popen(program_args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in blend_app.stdout:
            if type(line) == bytes:
                line = line.decode('utf-8')
            if line.strip().find('blinter') == 0:
                sys.stdout.write(line)
                sys.stdout.flush()

analyze_files(blend_files)
