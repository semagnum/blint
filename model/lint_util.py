"""Utility functions used in multiple files for importing and managing lint rules"""

import bpy


def security_check(expression: str):
    """Checks if there is insecure code, specifically `eval()` and `exec()`, otherwise returns nothing.

    :param expression: Python code in the form of a string.

    :raise ValueError: if expression contains insecure code.

    """
    if 'eval(' in expression or 'exec(' in expression:
        raise ValueError('Expression contains insecure code: {}'.format(expression))


def import_lint_rules(lint_rules: list[dict], rule_properties: bpy.props.CollectionProperty,
                      existing_rules: dict[str] = None, is_internal: bool = False):
    """Adds a list of rules to a bpy collection of LintRule items.

    :param lint_rules: lint rules to import.
    :param rule_properties: LintRule property collection.
    :param existing_rules: dict of existing rule names, to prevent duplicate additions.
    :param is_internal: shows whether the rules to be imported are from BLint or an external JSON file. Filters what rules are saved to external files.

    """
    if existing_rules is None:
        existing_rules = {}
    for rule in lint_rules:
        try:
            map(security_check, rule.values())
        except ValueError as ve:
            print(ve)
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
        new_rule.is_internal = is_internal
