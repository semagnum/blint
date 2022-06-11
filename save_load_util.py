from .model.lint_util import import_lint_rules
from .pref_util import get_user_preferences

import json
import bpy


def reload_rules(context):
    preferences = get_user_preferences(context)
    lint_collection = get_user_preferences(context).lint_rules

    import os
    dir_path = os.path.dirname(os.path.realpath(__file__))

    existing_rules = {rule.description: rule.enabled for rule in lint_collection.values()}

    lint_collection.clear()

    try:
        with open(os.path.join(dir_path, 'config.json'), 'r') as f:
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


def save_external_rules(context):
    preferences = get_user_preferences(context)
    lint_collection = get_user_preferences(context).lint_rules

    filepath = preferences.lint_filepath

    external_rules = []

    for rule in lint_collection.values():
        if rule.is_internal:
            continue
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

    real_path = bpy.path.abspath(filepath)
    with open(real_path, 'w') as f:
        json.dump({'rules': external_rules}, f, indent=4)