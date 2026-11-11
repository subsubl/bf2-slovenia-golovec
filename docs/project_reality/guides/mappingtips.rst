
Mapping Tips and Tricks
=======================

:Original Author: [R-DEV] IronTaxi (Retired)

This document provides a checklist for the map creation process, outlining the order of steps and linking to relevant resources.

General Resources
-----------------

**Editor Guide**

A basic user guide is available at :file:`.../Battlefield 2/bf2editor/Help/Workshop/LevelWorkshop.doc`.

Map Creation Checklist
----------------------

#. **Terrain**: Create the terrain layout. Options range from the basic terrain creation guide to advanced heightmap manipulation using tools such as `Terragen <http://bfeditor.org/forums/index.php?showtopic=2374&hl=terragen>`_.
#. **Terrain Texturing**: Apply color and detail textures to the terrain. Tools such as `TPaint <http://bfeditor.org/forums/index.php?showtopic=1716>`_ or `BF2Ecomap <http://bfeditor.org/forums/index.php?showtopic=3977>`_ can simplify this process.
#. **Objects and Configuration**: Place objects, configure spawn points, and set level properties.
#. **Overgrowth**: Configure vegetation assets.
#. **Undergrowth**: Configure ground-level vegetation assets.
#. **Roads**: Implement road networks.
#. **Water**: Define water settings.

   For example, you can extract the :file:`water.con` configuration file from an official map's :file:`server.zip` and adapt it for the map.

   .. describe:: water.con

      A configuration file used to define water settings.

#. **Gameplay Layers** (16, 32, or 64 player sizes):

   Configure the following elements:

   #. **Control Points**: Configure capture areas and object spawners.
   #. **Combat Area**: Define the map boundaries.
   #. **Commander Assets**: Place assets for commander use.

#. **Loading Screen**: Configure the loading screen, including the background, music, map image, and introduction text.
#. **Ambient Sounds**: Configure ambient soundscapes.
#. **Ambient Effects**: Implement environmental effects (e.g., birds).
#. **Sky Settings**: Configure skybox settings.

   For example, you can extract the :file:`sky.con` configuration file from an official map's :file:`server.zip` and adapt it for the map.

   .. describe:: sky.con

      A configuration file used to define skybox settings.

#. **Environmental Maps**: Configure environmental map settings.
#. **Lightmaps**: Bake lightmaps for the map.
#. **Ticket Ratio**: Set the ticket ratio for gameplay modes.
#. **Minimap**: Generate the map minimap.
#. **Singleplayer**: Configure singleplayer AI and setup.
#. **Final Packaging**: Pack the map using the Mod Manager. After packing, ensure the map folder contains only the following files and directories:

   .. describe:: server.zip

      A compressed archive containing server-side map assets.

   .. describe:: client.zip

      A compressed archive containing client-side map assets.

   .. describe:: info

      A directory containing map information.
