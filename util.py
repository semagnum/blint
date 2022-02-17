from .model.lint_util import import_lint_rules


def get_user_preferences(context):
    if hasattr(context, "user_preferences"):
        return context.user_preferences.addons[__package__].preferences

    return context.preferences.addons[__package__].preferences


def reload_rules(context):
    preferences = get_user_preferences(context)
    lint_collection = get_user_preferences(context).lint_rules

    import json
    import os
    import bpy
    dir_path = os.path.dirname(os.path.realpath(__file__))

    existing_rules = {rule.description: rule.enabled for rule in lint_collection.values()}

    lint_collection.clear()

    try:
        with open(os.path.join(dir_path, 'config.json'), 'r') as f:
            lint_rules = json.load(f)
            import_lint_rules(lint_rules.get('rules', []), lint_collection, existing_rules)
    except FileNotFoundError:
        print('No internal config.json found!')

    filepath = preferences.lint_filepath
    if filepath:
        real_path = bpy.path.abspath(filepath)
        with open(real_path, 'r') as f:
            rules = json.load(f)
            import_lint_rules(rules['rules'], lint_collection, existing_rules)
