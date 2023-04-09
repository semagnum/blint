import ast
import os
import zipfile

allowed_file_extensions = {'.py', '.json', '.md', 'LICENSE'}
exclude_folders = {'doc', 'venv', '.git', '.idea'}


def zipdir(path, ziph: zipfile.ZipFile, zip_subdir_name):
    for root, dirs, files in os.walk(path):
        root_path = str(root)
        if any(root_path.__contains__(folder_name) for folder_name in exclude_folders):
            continue

        for file in files:
            if str(file).startswith('.'):
                continue

            if any(file.endswith(ext) for ext in allowed_file_extensions):
                orig_hier = os.path.join(root, file)
                arc_hier = os.path.join(zip_subdir_name, orig_hier)
                ziph.write(orig_hier, arc_hier)


def generate_zip_filename(addon_name):
    major, minor, patch = get_addon_version('__init__.py')
    return '{}-{}-{}-{}.zip'.format(addon_name, major, minor, patch)


def get_addon_version(init_path):
    with open(init_path, 'r') as f:
        node = ast.parse(f.read())

    n: ast.Module
    for n in ast.walk(node):
        for b in n.body:
            if isinstance(b, ast.Assign) and isinstance(b.value, ast.Dict) and (
                    any(t.id == 'bl_info' for t in b.targets)):
                bl_info_dict = ast.literal_eval(b.value)
                return bl_info_dict['version']
    raise ValueError('Cannot find bl_info')


def zip_main(addon_name):
    filename = generate_zip_filename(addon_name)
    try:
        zipf = zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED)
        zipdir('.', zipf, addon_name)
        zipf.close()
        print('Successfully created zip file: {}'.format(filename))
    except Exception as e:
        print('Failed to create {}: {}'.format(filename, e))
        exit(1)


if __name__ == '__main__':
    zip_main('BLint')
