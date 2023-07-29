# Quickstart
See further details in the BLint docs at [semagnum.github.io/blint/](https://semagnum.github.io/blint/).

## Introduction

![BLint preferences window](/doc/img/preferences_window.png)

This addon allows users to run a series of checks on the Blender project
for the purpose of standardization and improving project file conventions.
Automated checks provided by BLint can speed up workflow and
automate continuous integration and quality checks before hitting 'Render'
or sending off to a render farm.
Quality checks may include but are not limited to:

- blend data naming conventions (no more 'Cube.025'!)
- checking render settings that may affect performance or expected results
- ensuring textures are all packed or located in a specific folder

In some cases, an issue can be easily fixed.
Each BLint rule has the option of implementing an automatic fix.
External configurations can be used as well as rules that come built-in with BLint.

These rules can be created with the edit rule section, or using the right-click context menu.
Create a rule enforcing a specific property's value in seconds!

![BLint rule creation in the right-click context menu](/doc/img/context_menu.png)

## Installation
1. Go to the main toolbar, select "Edit" and click "Preferences..."
2. Select the "Addons" section
3. Click "Install..." to open the file window
4. Select the zip file from your hard drive
5. Once the file window closes, the addon list should filter itself to only show BLint
6. Check the box to enable it.