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


import bpy
import json

from .. import get_user_preferences
from .save_load_util import import_lint_rules


def reload_issues(context):
    """Reload issues"""
    issues_collection = context.window_manager.lint_issues
    rules = get_user_preferences(context).lint_rules
    issues_collection.clear()
    for r in rules:
        for issue in r.get_issues():
            try:
                new_issue = issues_collection.add()
                new_issue.description = issue.get('description')
                new_issue.severity_icon = issue.get('severity_icon')
                new_issue.category_icon = issue.get('category_icon')
                new_issue.fix_expr = issue.get('fix_expr')
            except ValueError as e:
                print("Error with {}: {}".format(issue.get('description'), e))


def reload_rules(context):
    """Reloads rules from BLint's and external JSON file, if exists.

    :param context: Blender's context
    """
    preferences = get_user_preferences(context)
    lint_collection = get_user_preferences(context).lint_rules

    import os
    dir_path = os.path.dirname(os.path.realpath(__file__))

    existing_rules = {rule.description: rule.enabled for rule in lint_collection.values()}

    lint_collection.clear()

    try:
        with open(os.path.join(dir_path, '../config.json'), 'r') as f:
            lint_rules = json.load(f)
            import_lint_rules(lint_rules.get('rules', []), lint_collection, existing_rules, is_internal=True)
    except FileNotFoundError:
        print('No internal config.json found!')

    filepath = preferences.lint_filepath
    if filepath:
        real_path = bpy.path.abspath(filepath)
        with open(real_path, 'r') as f:
            rules = json.load(f)
            import_lint_rules(rules['rules'], lint_collection, existing_rules)
