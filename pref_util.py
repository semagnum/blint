def get_user_preferences(context):
    if hasattr(context, "user_preferences"):
        return context.user_preferences.addons[__package__].preferences

    return context.preferences.addons[__package__].preferences