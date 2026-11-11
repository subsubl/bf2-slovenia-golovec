
Importing Terrain into 3DsMax
=============================

After setting up the 3DsMax scene, navigate to :menuselection:`BF2 --> BF2 Lightmapping` and click :guilabel:`Load Land`. Browse to the map's folder at :file:`/pr_edit/levels/*your map*/` and open the :file:`Heightdata.con` file. The terrain import process will begin; this may take some time.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000013.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000014.jpg
   :align: center

.. note::

   If you encounter an "Out of scripter memory" error, open the :guilabel:`Listener Window` by pressing :kbd:`F11` and enter ``heapsize += 1000000000``. This should allow you to import the terrain successfully.

After the import is complete, your terrain will appear in the scene.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000015.jpg
   :align: center

To make the terrain easier to manage and prepare it for lightmapping, rename the terrain object from its default name (like ``Object01``) to ``_TERRAIN`` and convert it to an editable polygon.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000019.jpg
   :align: center

Next, apply an :guilabel:`Optimize Modifier` to the terrain. Set the :guilabel:`Face Thresh` to ``1`` to optimize the mesh without altering its shape.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000020.jpg
   :align: center

You may notice that the edges of your terrain (and possibly other areas) have imported with errors.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000315.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000316.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000319.jpg
   :align: center

While you can fix these errors manually in 3DsMax, they often originate from the heightmap itself. These errors can cause invisible walls that aircraft might crash into. It is best to fix them at the source.

Open your map's :file:`HeightmapPrimary.raw` file in Photoshop (remember to back it up first). Use the following settings: a channel count of :guilabel:`1`, a depth of 16 bits, and the byte order set to IBM PC.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000320.jpg
   :align: center

The heightmap will be displayed in grayscale, where white represents the highest points and black the lowest. You should be able to see the errors clearly along the edges.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000321.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000322.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000323.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000324.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000325.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000326.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000327.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000328.jpg
   :align: center

After editing, save the :file:`HeightmapPrimary.raw` file with the IBM PC Byte Order. It's a good idea to also save a :file:`.psd` version with your edits on a separate layer. Check the heightmap in the BF2 editor to ensure everything looks correct.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000329.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000330.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000331.jpg
   :align: center

You may want to manually smooth some of the edges to clean them up further.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000332.jpg
   :align: center

Once you are satisfied with your edits, save your terrain and compiled terrain in the editor.

   :menuselection:`File --> Re-Save` if you haven't made any edits

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000333.jpg
   :align: center

Now, delete the old terrain from your 3DsMax scene and re-import it using the steps above. The terrain should now be mostly clean. Minor imperfections are usually not a major concern.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000334.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000335.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000336.jpg
   :align: center

If you are happy with the result, optimize and rename the terrain object again. If not, repeat the editing process.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000337.jpg
   :align: center

Convert the terrain back to an editable polygon and apply an :guilabel:`Unwrap UVW` modifier to it.

#. :menuselection:`Modifier --> Edit`
#. Go to :guilabel:`Face Selection` Mode
#. Select all faces :kbd:`Ctrl-A`
#. On the right in the :guilabel:`Modifier` panel, in the :guilabel:`Map Parameters` rollout, hit the :guilabel:`Planar` button with :guilabel:`Normalized Map` checked

   This will apply UV coordinates to your terrain that match how it appears in-game.

#. Make sure that the North of your map is in the top of the UV etc
#. Once you are happy, click on the :guilabel:`Planar` button again and you can also uncheck :guilabel:`Show Pelt Seam` and :guilabel:`Show Map Seam` in the :guilabel:`Display` roll-out above it to make for easier viewing
#. Double-check that your UVs extend all the way to the very edge of the UV box

   To do this, select the bottom-left UV vertex and confirm its position is "U: 0.0, V: 0.0". Then check that the top-right vertex is at "U: 1.0, V: 1.0".

   If the UVs do not cover the entire UV space, the generated terrain shadows will be offset, and there will be a gap around the edges of your lightmap.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000338.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000339.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000340.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000343.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000342.jpg
   :align: center

When you are happy with the UVs, collapse the modifier. As an optional but recommended step, apply your minimap as a texture to the terrain. This helps verify that the UV map is correct and makes navigating your map easier.

#. Take a minimap render of your map in the editor
#. Save the minimap render as a :file:`.png`
#. Select an unused :guilabel:`Material` slot
#. Set the :guilabel:`Material` slot to use a :guilabel:`Standard Material` (should be by default)
#. Expand the :guilabel:`Maps Rollout`
#. Click on the :guilabel:`None` button next to :guilabel:`Diffuse Color`

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000022.jpg
   :align: center

#. Select :guilabel:`Bitmap` at the top of the list

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000347.jpg
   :align: center

#. Browse to your minimap file

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000023.jpg
   :align: center

Now,

#. Click :guilabel:`Go to Parent` in the top right, below the material slots, above the **Bitmap** button
#. Click the checkered-cube :guilabel:`Show Map in Viewport` button
#. Rename the material to something like ``Terrain``
#. Apply this material to your terrain

Now, you should see the minimap texture applied to your terrain.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000344.jpg
   :align: center

I recommend changing the terrain's object color from white to black. This will make it easier to distinguish from static objects (which import as white) when using edged or wireframe view modes.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000345.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000346.jpg
   :align: center

Finally, save your 3DsMax scene and create a backup before proceeding.
