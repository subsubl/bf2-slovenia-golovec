
Creating ZIP Files for Custom Content
=====================================

:Original Author: [R-DEV] J.F.Leusch69 (Retired)

This tutorial explains how to create ZIP files to include custom content, such as textures and static objects, in a map.

Requirements
------------

* A functional map.
* A compression tool (e.g., WinRAR or 7-Zip).
* Custom content assets.

Step 1: Creating the ZIP Files
------------------------------

Navigate to the map's folder and create the necessary ZIP files based on the type of custom content to be included.

.. describe:: common_client.zip

   Contains custom loading music, terrain textures, or sky textures. For the required internal directory structure, refer to :file:`common_client.zip` in the base Battlefield 2 installation (:file:`Battlefield2/mods/bf2`).

.. describe:: objects_client.zip

   Contains custom objects, including static objects, weapons, vehicles, and their associated textures. Refer to :file:`objects_client.zip` in the base Battlefield 2 installation for the required directory structure.

   The following file types should be included:

   * Meshes: :file:`.bundledmesh`, :file:`.staticmesh`, :file:`.skinnedmesh`
   * Textures: :file:`.dds`
   * Sounds: :file:`.ogg`, :file: `.wav`

   .. code-block:: text
      :caption: Example directory structure for meshes.

      staticobjects/pr/russia/houses/ru_house_01/meshes/ru_house_01.staticmesh

   .. code-block:: text
      :caption: Example directory structure for custom textures.

      staticobjects/common/textures/common_ch_billb_c_CuStOmSuFFiX.dds

   .. note::

      Custom woodland textures cannot override existing woodland textures.

.. describe:: objects_server.zip

   Contains server-side custom object data. Refer to :file:`objects_server.zip` in the base Battlefield 2 installation for the required directory structure.

   The following file types should be included:

   * Collision Meshes: :file:`.collisionmesh`
   * Configuration files: :file:`.con`
   * Tweak files: :file:`.tweak`

   .. code-block:: text
      :caption: Example directory structure.

      staticobjects/pr/russia/houses/ru_house_01/meshes/ru_house_01.collisionmesh
      staticobjects/pr/russia/houses/ru_house_01/ru_house_01.con
      staticobjects/pr/russia/houses/ru_house_01/ru_house_01.tweak

Step 2: Configuring Client/Server Archives
------------------------------------------

Download the :file:`Archives.zip` file, which contains :file:`ClientArchives.con` and :file:`ServerArchives.con`.

#. Identify the required configuration:

   * Use :file:`ClientArchives.con` when adding content client-side only (e.g., :file:`common_client.zip` or :file:`objects_client.zip`).
   * Use :file:`ServerArchives.con` when adding server-side content (e.g., new objects requiring collision meshes, tweaks, or configuration files).

#. Open the necessary :file:`ClientArchives.con` or :file:`ServerArchives.con` file.
#. Remove unnecessary lines.
#. Replace ``YoUr_lEvEl`` with the name of the map.

Step 3: Integrating Archives into the Map
-----------------------------------------

To load the custom content ZIP files:

#. Locate the :file:`server.zip` file in the map folder.
#. Place the required :file:`ClientArchives.con` or :file:`ServerArchives.con` file inside the :file:`server.zip` file.
