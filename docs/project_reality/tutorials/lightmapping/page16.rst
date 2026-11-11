
Combining & Splitting Terrain Lightmaps
=======================================

After generating the sun, sky, and water lightmaps for your terrain, combine them into a single file. Open both the :guilabel:`Sun & Sky` and the :guilabel:`Water` terrain lightmaps in Photoshop. Note that the terrain water lightmap should only contain red and black information.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000461.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000462.jpg
   :align: center

In the :guilabel:`Terrain Water` lightmap, navigate to the :guilabel:`Channels` tab, select the :guilabel:`Red` channel, select the entire canvas (:kbd:`Ctrl-A`), and copy it (:kbd:`Ctrl-C`).

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000463.jpg
   :align: center

Switch to the :guilabel:`Sun & Sky` terrain lightmap, navigate to its :guilabel:`Red` channel (which should be empty), and paste the copied :guilabel:`Red` channel from the water lightmap.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000464.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000465.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000466.jpg
   :align: center

Verify the result by switching to the RGB channels. The lightmap should appear combined. Save your lightmap with a descriptive name, such as :file:`_TERRAINLightingMap_Combined.tga`, ensuring it is saved as a 24-bit :file:`.tga` file.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000467.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000468.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000469.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000470.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000471.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000472.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000473.jpg
   :align: center

Once combined, split the terrain lightmap into smaller :file:`.dds` patches for the game. Download and install the splitting script provided by [R-DEV]AncientMan by extracting the folder within the :file:`.dds` file to your preferred location: :download:`SplitTgaToMultipleDDS.zip <https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/SplitTgaToMultipleDDS.zip>`

.. warning::

   The script may require the `Visual C++ Redistributable Packages <https://www.microsoft.com/en-gb/download/details.aspx?id=40784>`_ to function correctly.

Copy your combined terrain lightmap, :file:`_TERRAINLightingMap_Combined.tga`, into the script's :file:`input` folder.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000474.jpg
   :align: center

The tool defaults to an 8x8 (64 patch) setup for 2km x 2km and 4km x 4km maps. If you are working with a 1km map or smaller, you must adjust the script's settings, as these use a 4x4 (16 patch) setup.

.. important:: For 1km or smaller maps

   #. Open the :file:`SplitTgaToMultipleDds.bat` script in a text editor.
   #. Change :guilabel:`set num_x=8` and :guilabel:`set num_y=8` to :guilabel:`set num_x=4` and :guilabel:`set num_y=4`.

Maps smaller than 1km (e.g., 512m x 512m) likely use a 2x2 (4 patch) setup; verify this with your map files.

Once the input file is in place and the script is configured, run :file:`SplitTgaToMultipleDds.bat`. A command window will display the splitting process. Upon completion, all terrain lightmap patches will be located in a subfolder within the output folder, named after your :file:`.bat` file.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000475.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000476.jpg
   :align: center

Copy these patches into your :file:`\\mods\\pr_edit\\levels\\*YOUR MAP*\\Lightmaps` folder, overwriting any existing terrain lightmap patches.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000477.jpg
   :align: center

The following images show the results of the terrain lightmapping in the editor (note: transparent water is not visible in the editor, only in-game):

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000514.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000513.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000511.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000512.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000515.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000516.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000517.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000518.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000519.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000520.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000521.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000522.jpg
   :align: center
