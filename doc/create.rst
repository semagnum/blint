Rule Creation
=============

Before you can create your own rules,
you must create a config file to store them
and reference said file in your add-on preferences.
Create an empty text file, with the file extension ".json",
wherever you would like your rules stored.

See LintRules in :doc:`model` for more details on rule attributes and settings.

Using the form
------------------------------------

Once you reference the JSON file,
the rule creation form will be available in the preferences.
If you click "Reload rules", you will get an error - that's okay!
There's no rules in it yet, so of course it will fail. Your internal rules should still load.
Every time you create a rule, your JSON config file will be automatically updated and reloaded.

Once you have an external config saved,
you can create a new rule by opening the "Create Rules" dropdown and filling out the form.

Editing the JSON config
--------------------------------------------

Here's an example rule config file:

.. code-block:: json

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

Again, refer to LintRules in :doc:`model` for more details.

Rule Creation Tips
----------------------

- Blender can help you find the names of properties! Hover over a given property, right click and select "Copy Data Path" or "Copy Full Data Path". You can use this values in your form. Consider getting the path from Cycle's preview samples property:
  - "Copy Full Data Path" results in ``bpy.data.scenes["My Scene"].cycles.preview_samples`` - this is saying: go to my list of scenes, find the one named "My Scene", and access its Cycles preview samples property.
  - "Copy Data Path" results in ``cycles.preview_samples`` - notice the lack of scene specification. While this does not say what these attributes belong to, it's briefer and closer to what you need for a rule. Using the above data paths as an example, if your iterable expression is ``bpy.data.scenes`` and your variable name is ``var_scene``, then the reference you can use in an issue expression or fix statement for any given scene is ``var_scene.cycles.preview_samples``.
- Use the [bpy.context](https://docs.blender.org/api/current/bpy.context.html) module to get data relative to the current user state (``bpy.context.scene`` gets the currently visible scene, for example). For data that's project-wide, use the [bpy.data](https://docs.blender.org/api/current/bpy.data.html) module. For the icons, you can find a list of the Blender icons and their names from the built-in Blender addon, "Icon viewer."
- If you want a fix to match a change you have made in a Blend file, you can open Blender's "Info" editor window to see a list of actions you have done as a reference. It is even written like Python code!
- All the fields are checked for ``exec()`` or ``eval()`` to limit potential security vulnerabilities. However, these rules evaluate real Python code, so _be cautious with using others' rules that you're not familiar with.