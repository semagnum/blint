Install
========

1. Go to the main toolbar, select "Edit" and click "Preferences..."
2. Select the "Addons" section
3. Click "Install..." to open the file window
4. Select the zip file from your hard drive
5. Once the file window closes, the addon list should filter itself to only show BLint
6. Check the box to enable it.

If an error appears on this step, please report it.
Learn more [here](/blint/contribute#report-bugs).

Updating to a new version? Do this first!
------------------------------------------

1. Go to the main toolbar, select "Edit" and click "Preferences..."
2. Select the "Addons" section
3. Find the BLint addon in the addon list (you can use the search filter)
4. Click the dropdown arrow to expand the details on the BLint addon
5. Click the "Remove" button. If an error appears on this step, please report it.
6. Close Blender. Blender caches addons while it's running. The new version of the addon may not seem to be correct if you install immediately after.
7. Follow the installation instructions above

Okay, I installed BLint, where is it?
========================================

Go to the Properties editor window and click the "Scene" tab.
Here you will see the BLint panel. If you do not, it may be an error.
Learn how you can report it [here](/blint/contribute#report-bugs).

Scene panel
-------------

Every issue for your given file and context will be listed.
If a fix is provided for a given rule,
any issue belonging to that rule row will include a button to apply the fix to that specific issue.

Add-on preferences
--------------------

In the add-on preferences, you can enable, disable, or reload rules.
You can also add an external JSON file to create and save your own rules
(see how to create rules in [Create](/blint/create)).

Offline linting
-----------------

In the addon's ``offline`` folder contains python files that can be used to run blinter without Blender's GUI running.
Here's the syntax to run it:
``python offline_blinter.py <path\to\blender.exe> <path\to\file.blend or path\to\directory>``
It will run ``blinter_file_checker.py`` on each blend file. If given a single file, blinter will only run on that file.
If given a directory, blinter will find all ``.blend`` files within that directory as well as all subdirectories.

*Note: since Blender runs in the background, ``bpy.context`` may not be fully defined.
Lint rules relying on ``bpy.context`` may not find issues as expected.*