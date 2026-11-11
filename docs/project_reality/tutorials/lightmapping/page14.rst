
Terrain Sun & Sky Lightmaps
===========================

Configure the terrain for its sun and sky lightmaps. Note that the red channel is not used for point lights on the terrain; instead, it is used for water transparency, which is addressed later.

Load your map back into 3ds Max **9** and remove or disable any point lights, as they will conflict with the water depth lighting channel.

.. warning::

   If you require man-made (point) lighting on your terrain, incorporate them into your sky or sun light channels by making them blue or green. Note that this method prevents them from being disabled on day map layers, and they will inherit the same color and intensity as your sky or sun light.

Next, create a 'Sea Water Level' to ensure shadows are cast on the water's surface rather than the seabed.

#. Select the :guilabel:`_TERRAIN` mesh and add a :guilabel:`Volume Select` modifier.
#. Set the :guilabel:`Stack Selection Level` to :guilabel:`Vertex`.
#. Set the :guilabel:`Selection Method` to :guilabel:`Replace` and enable :guilabel:`Invert`.

This selects all vertices outside the :guilabel:`Volume Selection` box.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000266.jpg
   :align: center

Expand the modifier and, with the :guilabel:`Move Tool`` selected, switch the :guilabel:`Gizmo` to :guilabel:`Offset Mode Transform Type-in`.

Offset the :guilabel:`Volume Selection` box by your sea water depth. For a 5m sea water level, offset the box by 50 units (using the conversion: 10 units = 1m).

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000270.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000271.jpg
   :align: center

Enable :guilabel:`Percentage Snapping` and open the :guilabel:`Grid and Snap Settings` window (right-click the snapping button or navigate to :menuselection:`Customise --> Grid and Snap Settings`). In the :guilabel:`Options` tab, set the :guilabel:`Percent` box to :guilabel:`100%`.

Add an :guilabel:`Edit Poly` modifier to the terrain. In :guilabel:`Vertex Selection` mode, all vertices selected by the :guilabel:`Volume Select` modifier should be highlighted.

Using the :guilabel:`Scale` tool with :guilabel:`Percentage Snapping` enabled, select the :guilabel:`Z` axis and scale it to :guilabel:`0%` to flatten the selected vertices.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000272.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000273.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000275.jpg
   :align: center

Finally, use the :guilabel:`Move` tool and, in :guilabel:`Absolute Mode Transform Type-In`, set the :guilabel:`Z` value to your sea water level (e.g., 50 units for 5m).

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000277.jpg
   :align: center

The terrain at the sea water level should now be completely flat and at the correct depth.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000278.jpg
   :align: center

.. note::

   If you plan to re-lightmap any objects, ensure your sea water level does not cast shadows on them.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000279.jpg
   :align: center

With the :guilabel:`Terrain` selected, press :kbd:`0` (or navigate to :menuselection:`Render --> Render to Texture`) to open the :guilabel:`Render to Texture` window.

In the `General Settings` rollout, set the :guilabel:`Output` path:

#. Click the :guilabel:`...` button next to :guilabel:`Path`.
#. Browse to your lightmap scene folder.
#. Create and select a new :guilabel:`Terrain` folder.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000259.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000260.jpg
   :align: center

In the :guilabel:`Output` rollout, click :guilabel:`Add` and select :guilabel:`LightingMap`. The element will default to a :file:`.tga` format, which is appropriate.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000262.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000263.jpg
   :align: center

Adjust the element's width and height based on your map size and desired level of detail. A common standard is a terrain lightmap ratio of 2 pixels per meter. Use the following guidelines:

:1km x 1km: 2048 x 2048 (16 x 512x512 patches)
:2km x 2km: 4096 x 4096 (64 x 512x512 patches)
:4km x 4km: 8192 x 8192 (64 x 1024x1024 patches)

For a 4km x 4km map, use a width and height of 8192.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000265.jpg
   :align: center

Ensure all objects intended to cast shadows on the terrain are unhidden. This includes :guilabel:`LOD0` static meshes and the Overgrowth layer (with the correct leaf material applied).

Once settings are finalized, save your scene, perform a backup, and save a separate version for use in a newer version of 3ds Max (mandatory for renders of 8192 or larger).

Restart your computer and optimize your system as described in the object lightmapping section, then click :guilabel:`Render` in the :guilabel:`Render to Texture` window.

.. tip::

   For a better render preview, you can disable the diffuse texture for your terrain material. This will not affect the final lightmap.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000280.jpg
   :align: center

Rendering the sun and sky terrain lightmaps took approximately 2 hours and 7 minutes using :guilabel:`Adv. Ray Traced Shadows`. The following images show the successful results:

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_Terrain_Sun_LM.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_Terrain_Sky_LM.jpg
   :align: center
