# What does this addon do?

In IDEs like Visual Studio Code or PyCharm, the code can be analyzed with a linter to highlight bad practices, naming conventions, or potentially bad code.
BLinter allows users to run a series of checks on the Blender project for the purpose of standardization and improving project file conventions. Examples of this include:

- data naming conventions
- data values that affect performance or expected results
- ensuring textures are all packed or located in a specific folder

In some cases, an issue can be easily fixed. Each rule has the option of implementing an automatic fix. An external configuration can be used as well.

# How to use
In the preferences, you can enable or disable any given rule. There is also an option to link to an external json file.
Use the reload operator to refresh the rules list from both the external and internal config.

Go to the "Scene" tab and scroll to the BLint panel.
Every issue will be listed (if the panel is missing or empty, there is likely a parsing error with one of the rules - check the system console).
If a fix is provided for a given rule, there will also be a button to apply the fix for every issue belonging to that rule.

## Creating your own rules

Each rule should be defined as follows:

- enabled (optional) - a boolean that determines whether the rule is enabled by default. Defaults to `true`.
- description: a short description of the rule, listed with each issue.
- Severity icon (optional): the name of a Blender icon* used to display the severity of the issue, such as "INFO" or "ERROR". "INFO" is the default.
- Category icon: name of a Blender icon* used to display the category of the issue, such as "OBJECT_DATA".
- issue_expr: a Python expression that evaluates to True if the issue is present, False otherwise.
- fix_expr (optional): Python statement(s) that fix(es) the issue. A rule should only have a fix if it meets the following conditions (Otherwise, the resolution should be left to the user's discretion):
  - the fix will always work (no errors)
  - the fix is always what the user would want
  - the fix will remove the issue
- iterable_expr (optional): a string of Python code that evaluates to a list of  properties. If provided, multiple issues can be found from one rule.
- iterable_var (optional): when provided, any instance of `iterable_var` in `issue_expr` or `fix_expr` will be replaced with the value of `iterable_expr`. It is just a simple match replacement, so be careful (for example, the `iterable_var` "o" will replace every "o".)
- prop_label_expr (optional): If `iterable_var` is used, then `prop_label_expr` is the attribute of each iterable element to be used with the description. 
For example, "name" with `iterable_var` "bpy.data.objects" means that each object's `name` will be shown in the description). 
Otherwise, Python that evaluates it to a string used to label the issue.

Example Config:
```json
{
  "rules": [
    {
        "description": "Default cube exists",
        "severity_icon": "ERROR",
        "category_icon": "MESH_CUBE",
        "issue_expr": "'Cube' in bpy.context.scene.objects",
        "fix_expr": "bpy.ops.object.select_all(action='DESELECT'); bpy.context.scene.objects['Cube'].select_set(True); context.view_layer.objects.active = bpy.context.scene.objects['Cube']; bpy.ops.object.delete()",
        "prop_label_expr": ""
    },
    {
        "description": "\"Show in front\" set to on",
        "severity_icon": "INFO",
        "category_icon": "OBJECT_DATA",
        "iterable_expr": "bpy.context.scene.objects",
        "iterable_var": "obj",
        "issue_expr": "obj.show_in_front",
        "fix_expr": "obj.show_in_front = False",
        "prop_label_expr": "obj.name"
    }
  ]
}
```

Use the internal config as a guide. Remember that you can right-click on any Blender property and use the "Copy (full) data path" to get the necessary `bpy` syntax.

Use the [bpy.context](https://docs.blender.org/api/current/bpy.context.html) module to get data relative to the current user state (`bpy.context.scene` gets the currently visible scene, for example). For data that's project-wide, use the [bpy.data](https://docs.blender.org/api/current/bpy.data.html) module.
For the icons, you can find a list of the Blender icons and their names from the built-in Blender addon, "Icon viewer."

All the fields are checked for `exec()` or `eval()` to limit potential vulnerabilities. However, these rules evaluate real Python code, so _be cautious with using others' rules that you're not familiar with_.