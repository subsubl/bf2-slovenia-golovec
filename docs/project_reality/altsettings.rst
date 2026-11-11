
Alternate Settings for Gameplay Layers
======================================

:Original Author: [R-DEV] VapoMan (Retired)

Loading alternate files with different settings for gameplay layers allows for different teams, static objects, and sky settings without cloning a map. This is achieved by configuring a gameplay layer to load an :file:`init.con` file, which then loads the necessary alternate files.

For implementation examples, refer to existing Project Reality maps such as :file:`Operation Marlin`, :file:`Kokan`, :file:`Ramiel`, or :file:`Al Basrah`.

Using Alternate Teams
---------------------

To use alternate teams, create a text document in the map folder and add the following code:

.. code-block:: text

   run ../../Factions/faction_init.con 1 "opfor"
   run ../../Factions/faction_init.con 2 "blufor"

Update the team names to the desired factions. Include both teams in the initialization, even if only one faction requires modification.

For a complete list of team names and additional information on the initialization system, see the following resource:

`[0957] Init System <https://www.realitymod.com/forum/f354-community-maps/89720-0957-init-system.html#post1475836>`_

Save the file as :file:`Init_X.con`, where ``X`` represents the faction name, layer name, or game mode (e.g., :file:`Init_canada.con`, :file:`Init_32.con`, or :file:`Init_skirmish.con`).

.. note::

   Alternate teams use the same voice profiles as the original teams. For example, if the default team 2 is USA, any alternate team 2 will use USA voice profiles (e.g., USMC or Canada).

Altering Other Files
--------------------

This method also applies to alternate sound settings, :file:`AmbientObjects`, :file:`Triggerables`, and :file:`SoundDistances`.

#. **Back up existing files**: Create copies of :file:`sky.con` and :file:`water.con`.
#. **Configure settings**: Use the editor to adjust the lighting and water settings.
#. **Save and rename**: Save the modified :file:`sky.con` as :file:`sky_X.con` and the modified :file:`water.con` as :file:`water_X.con`. Replace ``X`` with a descriptive name for the sky setting, layer, or game mode (e.g., :file:`sky_night.con`, :file:`sky_cloudy.con`, :file:`sky_32.con`, or :file:`sky_skirmish.con`).

.. note::

   Use a single set of lightmaps. Ensure sun and moon positions remain consistent across different sky settings. Adjust water settings to match the new lighting conditions when necessary.

Using Additional Static Objects
-------------------------------

Alternate :file:`staticobjects.con` files can add objects to a map, but they cannot remove existing objects from the original :file:`staticobjects.con`.

#. **Back up existing files**: Create a copy of the original :file:`staticobjects.con`.
#. **Configure settings**: Use the editor to add the desired objects and save.
#. **Create the alternate file**: In the new :file:`staticobjects.con`, remove all content except for the newly added objects. Place these objects at the end of the document.
#. **Configure loading**: At the top of the document, include the directory paths for the loaded static objects:

   .. code-block:: text

      if v_arg1 == BF2Editor
         console.allowMultipleFileLoad 0
         run /objects/staticobjects/common/object.con
         console.allowMultipleFileLoad 1
      endIf

   Include only the alternate objects that are not present in the original :file:`staticobjects.con`.

#. **Save and rename**: Save the file as :file:`staticobjects_X.con` (e.g., :file:`staticobjects_32.con`, :file:`staticobjects_skirmish.con`, or :file:`staticobjects_insurgency.con`). Restore the original :file:`staticobjects.con` from the backup.

Creating an Alternate Init.con
------------------------------

The alternate :file:`init.con` file loads all required alternate files. Include only the lines of code for the elements being modified (e.g., alternate teams, texture suffixes, or camera positions).

#. **Create a new text document** and include the following template:

   .. code-block:: text

      if v_arg1 == BF2Editor
         run StaticObjects_X.con BF2Editor
         run Sounds_X.con
         run Sky_X.con BF2Editor
         run AmbientObjects_X.con BF2Editor
         run Water_X.con
         run TriggerableTemplates_X.con BF2Editor
      else
         run Sky_X.con v_arg2
         run Sounds_X.con
         run SoundDistances_X.con
         run AmbientObjects_X.con
         run Water_X.con
         run TriggerableTemplates_X.con
      endIf

      rem ------------------------------- LevelSettings -------------------------------
      rem -----------------------------------------------------------------------------

      run ../../Factions/faction_init.con 1 "opfor"
      run ../../Factions/faction_init.con 2 "blufor"

      rem -----------------------------------------------------------------------------

      gameLogic.setBeforeSpawnCamera -300/33/139 86/-1/0

      if v_arg1 == BF2Editor
         LevelSettings.CustomTextureSuffix "marlin"
      else
         texturemanager.customTextureSuffix "marlin"
      endIf
      rem -----------------------------------------------------------------------------

      GameLogic.MaximumLevelViewDistance 600

      rem -----------------------------------------------------------------------------

.. describe:: v_arg1

   A variable passed to the initialization script. When set to ``BF2Editor``, the script executes in the context of the editor; otherwise, it executes in the game client.

.. describe:: v_arg2

   A variable passed to the initialization script, typically used to specify the sky setting or other environmental parameters during gameplay.

.. describe:: LevelSettings.CustomTextureSuffix

   A configuration parameter used to define a custom texture suffix for the level.

.. describe:: GameLogic.MaximumLevelViewDistance

   A configuration parameter that sets the maximum view distance for the level.

#. **Customize the template**: Remove the lines that do not apply to your specific modifications. Replace ``X`` with the name used for your alternate files.
#. **Save the file**: Save the file as :file:`init_X.con`, using the same identifier used for the associated files.

Loading the Alternate Init.con via gameplayobjects.con
------------------------------------------------------

To activate the alternate initialization, modify the :file:`gameplayobjects.con` file for the target gameplay layer:

#. Open the :file:`gameplayobjects.con` file.
#. Insert the following line at the beginning of the file:

   .. code-block:: text

      run ../../../Init_X.con

#. Replace ``X`` with the name of your alternate initialization file and save.

Multiple alternate files and initialization files can be loaded across different gameplay layers by adjusting the filenames and code lines accordingly.
