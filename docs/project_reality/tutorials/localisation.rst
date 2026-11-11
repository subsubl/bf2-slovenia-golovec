
Map Localization Guide
======================

:Original Author: AncientMan

Localization controls the in-game text, such as heads-up display (HUD) elements, menus, and control point names. This guide outlines how to implement localization for custom maps.

Setting Up Localization
-----------------------

To prevent interference with standard game files, create a unique localization file for your map (e.g., :file:`community_op_barracuda.utxt`).

#. Copy an existing :file:`.utxt` file (such as :file:`prmaps.utxt`).
#. Delete all existing content, preserving only the first two lines to maintain the required format.
#. Add your map name using the following structure:

   .. code-block:: text

      HUD_LEVELNAME_mapname                                 Map Display Name

Ensure the localization ID (e.g., `community_op_barracuda`) matches your map folder name, and set the display name as defined in your map's :file:`.desc` file.

Naming Conventions
------------------

Consistent naming is essential for control points and other localized elements. Use the following format based on the game mode and layer:

.. code-block:: text

   cpname_mapfolder_gamemode_cpname

.. code-block:: text
   :caption: Example

   cpname_community_op_barracuda_aas64_missilesilo

Implementation Steps
--------------------

#. **Locate GameplayObjects**: Open your map's :file:`GamePlayObjects.con` file.
#. **Rename Identifiers**: Use a text editor to find and replace existing control point names with your new, formatted names. Be cautious with "replace all" operations to avoid accidentally renaming other objects like spawn points that may share similar names.
#. **Verify IDs**: Ensure no two control points share the same ID, as this will cause conflicts.
#. **Update Localization File**: Map your new control point IDs to their in-game display names:

   .. code-block:: text

      cpname_community_op_barracuda_aas64_missilesilo                      PLA Missile Silo

.. note::

   * **Spacing**: Use spaces, not tabs, between the ID and the display name. Tabs can cause parsing errors.
   * **Internationalization**: It is recommended to copy your localization file into all language subdirectories (e.g., :file:`/localization/chinese/`). While translation is not necessary, providing the file in all language folders ensures players using non-English game settings see the correct labels.
