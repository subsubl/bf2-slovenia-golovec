
Expanding a Map from Scale 2 to Scale 4
=======================================

:Original Author: [R-DEV] J.F.Leusch69 (Retired)

.. note::

   The original version of this tutorial contains images that are no longer available.

This tutorial describes the process of expanding a map from scale 2 to scale 4 (for example, expanding a 2x2 km map to a 4x4 km map). This method preserves static objects, ambient objects, sound configurations, and overgrowth.

.. important::

   This process involves significant modifications, including the potential loss of color, light, and detail maps. Create a complete backup of the map before proceeding.

Prerequisites
-------------

* Knowledge of the Battlefield 2 Editor and the :file:`pr_edit` mod configuration.
* Understanding of how to edit :file:`terrain.con` to enable scale 4 map functionality.

Selecting a Map
---------------

The ideal candidates for this expansion are 2x2 km maps (e.g., :file:`Daqing Oilfields`, :file:`Ramiel`, or :file:`Qwai`).

Verify the current map size by checking the :file:`Heightdata.con` file, located in the map's folder (or within :file:`server.zip`). The relevant parameters are:

.. describe:: heightmapcluster.setHeightmapSize

   Indicates the total map size (e.g., 2048 for a 2 km map).

.. describe:: heightmap.setSize

   Indicates the heightmap resolution (e.g., 1025 for a 2 km map, calculated as 1024 + 1).

.. describe:: heightmap.setScale

   Defines the scale factors for the terrain and height.

Editing the Heightmap
---------------------

#. Unpack :file:`client.zip` and :file:`server.zip` if necessary, and ensure files are not Read-Only.
#. Copy :file:`HeightmapPrimary.raw` to a new file (e.g., :file:`4x4km.raw`).
#. Open both files in Photoshop (or an alternative raw file editor).
#. Resize :file:`HeightmapPrimary.raw` to 50% of the original size.
#. In :file:`4x4km.raw`, set the :guilabel:`Alpha 1` channel to solid black and the :guilabel:`Alpha 2` channel to 75% gray.
#. Copy the channels from the resized :file:`HeightmapPrimary.raw` to the corresponding channels in :file:`4x4km.raw`, centering them.
#. Save :file:`4x4km.raw` as :file:`HeightmapPrimary.raw`, overwriting the original file.

Editing Configuration Files
---------------------------

Update :file:`Heightdata.con` to reflect the new dimensions and scale:

* Change ``heightmapcluster.setHeightmapSize`` (e.g., to 4096).
* Update ``heightmap.setScale`` values to reflect the new scale factors.
* Update ``heightmap.setScale`` for secondary heightmaps.

Finalizing
----------

#. Load the map in the editor.
#. The terrain will require smoothing and manual adjustment due to the expanded scale.
#. Use the editor tools to refine the terrain.
