def security_check(expression: str):
    """Checks if there is insecure code, specifically ``eval()`` and ``exec()``, otherwise returns nothing.

    :param expression: Python code in the form of a string.

    :raise ValueError: if expression contains insecure code.

    """
    if 'eval(' in expression or 'exec(' in expression:
        raise ValueError('Expression contains insecure code: {}'.format(expression))
