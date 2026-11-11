
Manual Overgrowth and Undergrowth Atlas Configuration
=====================================================

:Original Author: [R-DEV] AFsoccer (Retired)

.. important::

   The original version of this documentation contained images that are no longer available.

Purpose
-------

Manual hand-packing of Overgrowth (OG) and Undergrowth (UG) atlases replaces the automatically generated versions produced by the Battlefield 2 Editor. This process should be the final step before a map is released, as any subsequent additions or removals of vegetation items will require the atlas to be re-created.

Overgrowth (OG) and Undergrowth (UG) Atlases
--------------------------------------------

Battlefield 2 uses texture palettes for vegetation objects to provide color and detail. To optimize performance, the engine aggregates these textures into a single texture palette called an "atlas".

Editor-generated atlases often contain significant empty space and can cause "texture bleeding," where a solid texture bleeds into adjacent textures, resulting in visible dark lines around objects. Hand-packing the atlas allows for:

* **Efficient texture placement**: Maximizes the use of available space.
* **Removal of empty space**: Reduces memory footprint.
* **Prevention of bleeding**: Organizes solid textures to prevent bleeding.

The procedure for hand-packing Undergrowth (UG) atlases is identical to the procedure for Overgrowth (OG) atlases.

Requirements
------------

* A raster-graphics editor (e.g., Adobe Photoshop, GIMP).
* :file:`.dds` plug-ins (e.g., NVIDIA Texture Tools for Adobe Photoshop).

Step 1: Generate the OG Atlas
-----------------------------

#. Open the map in the Battlefield 2 Editor.
#. Ensure all overgrowth and hand-placed overgrowth statics are loaded, as their textures must be included in the atlas.
#. Select :menuselection:`Compile --> Generate Overgrowth Atlas`.
#. Close the editor once the process is complete.

Step 2: Review the OG Atlas
---------------------------

The atlas file is located in the map's overgrowth folder and is named :file:`OvergrowthAtlas0.dds`. Review the file for wasted space or solid textures positioned adjacent to transparent textures.

To check transparency:

#. Open the file in Photoshop or GIMP.
#. Select the :guilabel:`Channels` tab.
#. Select :guilabel:`Alpha 1`. White areas are opaque; black areas are transparent.

Step 3: Determine New Atlas Size
--------------------------------

If optimization is required, determine the new atlas dimensions. Check the existing atlas dimensions via :menuselection:`Image --> Image Size`. Standard atlas dimensions are powers of two (e.g., 256, 512, 1024, or 2048). Ensure the new dimensions are sufficient to accommodate all textures while minimizing wasted space.

Step 4: Prepare Photoshop
-------------------------

#. Create a new Photoshop document with the target dimensions.
#. Configure a grid by selecting :menuselection:`Edit --> Preferences --> Guides, Grid & Slices`. Set the grid spacing based on a percentage (e.g., a number that is 1/4, 1/8, or 1/16 of 100%).
#. In the :menuselection:`View` menu, ensure :guilabel:`Ruler`, :guilabel:`Extras`, and :guilabel:`Snap` (with :guilabel:`Grid` checked) are enabled.
#. Configure the ruler to display percentages by right-clicking the ruler and selecting :guilabel:`percent`.

Step 5: Analyze the .tai File
-----------------------------

The :file:`OvergrowthAtlas.tai` file in the map's overgrowth folder organizes the atlas.

.. code-block:: text
   :caption: .tai file format

   # <filename>        <atlas filename>, <atlas idx>, <woffoffset>, <hoffoffset>, <width>, <height>

The file contains the following information for each entry:

.. describe:: Atlas index

   Indicates the atlas file (e.g., :file:`OvergrowthAtlas0.dds`).

.. describe:: Location

   The texture position on the atlas, using a top-left (0,0) coordinate system based on percentage.

.. describe:: Size

   The texture size on the atlas, based on a percentage of the atlas dimensions.

Step 6: Create the New Atlas
----------------------------

#. Create a new "Alpha 1" channel in Photoshop via the :guilabel:`Channels` tab.
#. Arrange textures, placing the largest textures first.
#. Place solid textures last to separate them from non-solid textures and prevent bleeding.
#. Copy and paste the RGB and Alpha 1 data separately for each texture. Use the grid to snap textures into position.
#. Update the :file:`OvergrowthAtlas.tai` file to reflect the new coordinates and sizes of each texture on the atlas.
#. Ensure solid textures do not border non-solid textures or atlas edges. If placing a solid object on the edge, ensure the opposing edge remains empty or contains another solid object to prevent tiling issues.

Step 7: Saving
--------------

Save all atlases as :file:`.dds` files using the **DXT5 ARGB (8 bpp | interpolated alpha)** format with 10 Mipmaps. Retain the :file:`.PSD` file for future adjustments.

Step 8: Implementation
----------------------

#. Set the new :file:`.dds` and :file:`.tai` files to **Read Only**.
#. Place the files in the map's overgrowth folder (for OG) or the main map folder (for UG).
#. Open the editor and re-save the OG and UG to ensure the changes are applied.
#. Test the map in-game to verify that the textures display correctly.
