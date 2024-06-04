# Copyright (C) 2024 Spencer Magnusson
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

import json
import logging
import os

import bpy

from .pref_access import get_user_preferences
from .security import security_check

log = logging.getLogger(__name__)


def get_config_filepath(context):
    """Gets the currently set rule config file."""
    preferences = get_user_preferences(context)
    if preferences.config_type == 'INTERNAL':
        dir_path = os.path.dirname(os.path.realpath(__file__))
        config_filepath = os.path.join(dir_path, '../config.json')
    else:
        config_filepath = bpy.path.abspath(preferences.lint_filepath)

    return config_filepath


def does_config_exist(context):
    """Checks if rule config file is set and exists as a file."""
    return os.path.isfile(get_config_filepath(context))


def import_lint_rules(lint_rules: list[dict], rule_properties: bpy.props.CollectionProperty,
                      existing_rules: dict[str] = None,):
    """Adds a list of rules to a bpy collection of LintRule items.

    :param lint_rules: lint rules to import.
    :param rule_properties: LintRule property collection.
    :param existing_rules: dict of existing rule names, to prevent duplicate additions.

    """
    if existing_rules is None:
        existing_rules = {}
    for rule in lint_rules:
        try:
            map(security_check, rule.values())
        except ValueError as ve:
            error_message = 'Rule \"' + rule.get('description', 'Unknown rule') + '\": ' + str(ve)
            log.error(error_message)
            continue

        new_rule = rule_properties.add()
        new_rule.description = rule.get('description')
        if new_rule.description in existing_rules and not existing_rules[new_rule.description]:
            new_rule.enabled = False
        else:
            new_rule.enabled = rule.get('enabled', True)
        new_rule.severity_icon = rule.get('severity_icon', 'INFO')
        new_rule.category_icon = rule.get('category_icon')
        new_rule.issue_expr = rule.get('issue_expr')
        new_rule.fix_expr = rule.get('fix_expr', '')
        new_rule.prop_label_expr = rule.get('prop_label_expr', '')
        new_rule.iterable_var = rule.get('iterable_var', '')
        new_rule.iterable_expr = rule.get('iterable_expr', '')


def save_external_rules(context):
    """Saves rules to external JSON file.

    :param context: Blender's context
    """
    lint_collection = get_user_preferences(context).lint_rules

    filepath = get_config_filepath(context)

    external_rules = []

    for rule in lint_collection.values():
        new_rule = {
            'description': rule.description,
            'enabled': rule.enabled,
            'severity_icon': rule.severity_icon,
            'category_icon': rule.category_icon,
            'issue_expr': rule.issue_expr,
            'prop_label_expr': rule.prop_label_expr,
        }
        if rule.fix_expr:
            new_rule['fix_expr'] = rule.fix_expr
        if rule.iterable_expr:
            new_rule['iterable_expr'] = rule.iterable_expr
            new_rule['iterable_var'] = rule.iterable_var
        external_rules.append(new_rule)

    with open(filepath, 'w') as f:
        json.dump({'rules': external_rules}, f, indent=4)
