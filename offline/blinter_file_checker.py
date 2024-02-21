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


"""Python file to run within Blender to run BLint.

If you wish to run BLint without opening Blender, use ``offline_blinter.py``.

"""
import sys
import bpy


def log(line: str):
    """Adds BLint prefix for logging.

    :param line: line to print.
    """
    if line[-1] != '\n':
        line += '\n'
    print('BLint: ' + line)


def print_issues(issue_iter: list['LintIssue'], issue_order: list[tuple]):
    """Prints all issues.

    :param issue_iter: list of issues
    :param issue_order: indices determining order to print issue
    """
    for idx, _, _ in issue_order:
        issue = issue_iter[idx]
        log('{}\t{}'.format(issue.severity_icon, issue.description))


def fix_issues(issue_iter):
    """Runs fixes on each issue that has a fix option.

    :param issue_iter: list of issues
    """
    orig_num_issues = len(issue_iter)
    bpy.ops.scene_analyzer.fix_issue_all()
    reload_issues(context)
    curr_issues = window_manager.lint_issues
    curr_num_issues = len(curr_issues)
    num_fixed = orig_num_issues - curr_num_issues
    log('{} issues fixed'.format(num_fixed))
    bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
    log('File saved')


if __name__ == '__main__':
    auto_fix = any('--blint-fix' == a for a in sys.argv)

    # get lint rules from preferences
    blend_filename = bpy.data.filepath
    try:
        from blint.model.lint_issue import get_sort_value
        from blint.save_load import reload_issues
    except ImportError:
        log('blint not found, the blint addon must be installed and enabled!')
        sys.exit(1)

    context = bpy.context
    window_manager = context.window_manager

    context.scene.render.engine = 'CYCLES'

    reload_issues(context)

    # print blender file name
    try:
        if len(window_manager.lint_issues) == 0:
            log('No issues found')
        else:
            issues = window_manager.lint_issues
            issue_sort_vals = [(idx, get_sort_value(issue), issue.description) for idx, issue in enumerate(issues)]
            issue_sort_vals.sort(key=lambda x: (x[1], x[2]))
            print_issues(issues, issue_sort_vals)

            num_fixable = len([True for issue in issues if issue.fix_expr])
            if num_fixable > 0:
                if auto_fix:
                    log('Fixing {} of {} issues...'.format(num_fixable, len(issues)))
                    fix_issues(issues)
                    reload_issues(context)
                else:
                    log('{} of {} issues can be automatically fixed'.format(num_fixable, len(issues)))

    except Exception as e:
        log(str(e))

    log('Closing file...')
