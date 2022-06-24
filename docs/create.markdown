---
# title: Use
---

## Create

1. [Setup](#setup)
2. [Creating Rules by form](#form)
3. [Creating Rules by JSON](#json)
4. [Other Tips](#tips)

## Setup {#setup}

Before you can create your own rules,
you must create a config file to store them
and reference said file in your add-on preferences.
Create an empty text file, with the file extension ".json",
wherever you would like your rules stored.

Once you reference it in the add-on preferences, 
the rule creation subpanel will be enabled.
If you click "Reload rules", you will get an error - that's okay!
There's no rules in it yet, so of course it will fail. Your internal rules should still load.
Every time you create a rule, your JSON config file will be automatically updated and reloaded.


## Creating rules with the form {#form}
Once you have an external config saved,
you can create a new rule by opening the "Create Rules" dropdown and filling out the form.
Here are the properties:

- **Enabled by default** - determines whether the rule is enabled by default. Defaults to `true`.
- **Description**: a short description of the rule, listed with each issue.
- **Severity icon**: the string name of a Blender icon* used to display the severity of the issue.
The following icons available: `[ERROR, INFO]`, with errors shown at the top.
"INFO" is the default.
- **Category icon**: name of a Blender icon* used to display the category of the issue, such as "OBJECT_DATA".
- **Iterable expression**: Python code that evaluates to a list of Blend data
(such as each scene or object in a blend file).
If provided, multiple issues can be found from one rule.
- **Iterable variable**: variable name that can be used to reference an element.
If you provide `my_scene`, you can use `my_scene` to reference any given scene in your issue expression and fix statements.
Note: The algorithm relies on a simple text replacement for the issue and fix expressions, so be careful
(for example, an iterable variable "o" will replace every "o" in the issue expression and fix statement, which can be problematic.)
- **Iterable identifier expression**: the attribute of each iterable element to be used with the description.
`name` is default.
- **Issue expression**: a Python expression that evaluates to `True` if the issue is present, `False` otherwise.
- **Fix statements (optional)**: Python statement(s) that fix(es) the issue. A rule should only have a fix if it meets the following conditions (Otherwise, the resolution should be left to the user's discretion):
  - the fix will always work (no errors)
  - the fix is always what the user would want
  - the fix will remove the issue


## Creating rules by editing the JSON config {#json}
Each rule should be defined as follows:

- `enabled` (optional) - a boolean that determines whether the rule is enabled by default. Defaults to `true`.
- `description`: a short description of the rule, listed with each issue.
- `severity_icon` (optional): the name of the Blender icon used to display the severity of the issue.
The following icons available: `[ERROR, INFO]`, with errors shown at the top of the issues list.
"INFO" is the default.
- `category_icon`: name of a Blender icon* used to display the category of the issue, such as "OBJECT_DATA".
- `iterable_expr` (optional): a string of Python code that evaluates to a list of  properties. If provided, multiple issues can be found from one rule.
- `iterable_var` (optional): when provided, any instance of `iterable_var` in `issue_expr` or `fix_expr` will be replaced with the value of `iterable_expr`. It is just a simple match replacement, so be careful (for example, the `iterable_var` "o" will replace every "o".)
- `prop_label_expr` (optional): If `iterable_var` is used, then `prop_label_expr` is the attribute of each iterable element to be used with the description. 
For example, "name" with `iterable_var` "bpy.data.objects" means that each object's `name` will be shown in the description). 
Otherwise, Python that evaluates it to a string used to label the issue.
- `issue_expr`: a Python expression that evaluates to True if the issue is present, False otherwise.
- `fix_expr` (optional): Python statement(s) that fix(es) the issue. A rule should only have a fix if it meets the following conditions (Otherwise, the resolution should be left to the user's discretion):
  - the fix will always work (no errors)
  - the fix is always what the user would want
  - the fix will remove the issue

Example Config:
```json
{
  "rules": [
    {
        "description": "Default cube exists",
        "severity_icon": "ERROR",
        "category_icon": "MESH_CUBE",
        "issue_expr": "'Cube' in bpy.data.objects",
        "fix_expr": "bpy.data.objects.remove(objs[\"Cube\"], do_unlink=True)",
        "prop_label_expr": ""
    },
    {
        "description": "\"Show in front\" set to on",
        "severity_icon": "INFO",
        "category_icon": "OBJECT_DATA",
        "iterable_expr": "bpy.data.objects",
        "iterable_var": "obj",
        "issue_expr": "obj.show_in_front",
        "fix_expr": "obj.show_in_front = False",
        "prop_label_expr": "obj.name"
    }
  ]
}
```

## Rule development tips {#tips}

- Blender can help you find the names of properties!
Hover over a given property, right click and select "Copy Data Path" or "Copy Full Data Path".
You can use this values in your form. Consider getting the path from Cycle's preview samples property:
  - "Copy Full Data Path" results in `bpy.data.scenes["My Scene"].cycles.preview_samples` -
this is saying: go to my list of scenes, find the one named "My Scene",
and access its Cycles preview samples property.
  - "Copy Data Path" results in `cycles.preview_samples` - notice the lack of scene specification.
While this does not say what these attributes belong to,
it's briefer and closer to what you need for a rule.

  Using the above data paths as an example,
if your iterable expression is `bpy.data.scenes` and your variable name is `var_scene`,
then the reference you can use in an issue expression or fix statement for any given scene is `var_scene.cycles.preview_samples`.
- Use the [bpy.context](https://docs.blender.org/api/current/bpy.context.html) module to get data relative to the current user state (`bpy.context.scene` gets the currently visible scene, for example). For data that's project-wide, use the [bpy.data](https://docs.blender.org/api/current/bpy.data.html) module.
For the icons, you can find a list of the Blender icons and their names from the built-in Blender addon, "Icon viewer."
- If you want a fix to match a change you have made in a Blend file, you can open Blender's "Info" editor window to see a list of actions you have done as a reference. It is even written like Python code!
- All the fields are checked for `exec()` or `eval()` to limit potential security vulnerabilities. However, these rules evaluate real Python code, so _be cautious with using others' rules that you're not familiar with_.