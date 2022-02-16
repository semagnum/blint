from .LintRule import LintRule


def security_check(expression: str):
    if 'eval(' in expression or 'exec(' in expression:
        raise ValueError('Expression contains insecure code: {}'.format(expression))


def import_lint_rules(lint_rules, collection_properties):
    for rule in lint_rules:
        try:
            map(security_check, rule.values())
        except ValueError as ve:
            print(ve)
            continue
        new_rule: LintRule = collection_properties.add()
        new_rule.description = rule.get('description')
        new_rule.severity_icon = rule.get('severity_icon', 'INFO')
        new_rule.category_icon = rule.get('category_icon')
        new_rule.issue_expr = rule.get('issue_expr')
        new_rule.fix_expr = rule.get('fix_expr', '')
        new_rule.prop_label_expr = rule.get('prop_label_expr', '')
        new_rule.iterable_var = rule.get('iterable_var', '')
        new_rule.iterable_expr = rule.get('iterable_expr', '')
