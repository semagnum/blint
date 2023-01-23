def get_user_preferences(context):
    """Returns BLint preferences and attributes.

    :param context: Blender's context
    """
    if hasattr(context, "user_preferences"):
        return context.user_preferences.addons[__package__].preferences

    return context.preferences.addons[__package__].preferences