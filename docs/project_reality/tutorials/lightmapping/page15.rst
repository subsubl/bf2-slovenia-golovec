
Terrain Sea Water Depth/Transparency Lightmap
=============================================

Configure the terrain's water transparency lightmap. Unlike statics, where the red channel is used for point lighting, the red channel in the terrain lightmap controls water transparency based on depth.

Load your lightmapping scene back into 3ds Max **9**. Download and merge the :file:`_WaterLight` template into your scene using the same method as your sky lights: :download:`Lightmaps_Water_Light_Template.max <https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Lightmaps_Water_Light_Template.max>`

This is a :guilabel:`Target Direct` light, similar to your sun light, but it is positioned in the center of your map and points directly downwards. By default, the light is at :guilabel:`0, 0, 50` (X, Y, Z). Adjust the :guilabel:`Z`-axis value to match your sea water level (e.g., 50 units for 5m).

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000453.jpg
   :align: center

The light is configured to cast no shadows and uses the correct red light channel. You may wish to adjust the :guilabel:`Near Attenuation` settings, which control the start and end of the transparency. The :guilabel:`End` setting determines when the water becomes completely opaque.

In the BF2 Editor, water typically becomes opaque at around 3.5m. To make the water more transparent, increase the :guilabel:`End` value; to make it less transparent, decrease it. For a tropical map with clear water, an :guilabel:`Near Attenuation` :guilabel:`End` value of :guilabel:`45` (4.5m) might be appropriate.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000454.jpg
   :align: center

Turn off all other lights in your map. If the viewport turns black and you wish to see your map again:

#. :kbd:`Right-Click` on :guilabel:`Perspective` in the top-left of your viewport.
#. Select :guilabel:`Configure`.
#. In the :guilabel:`Rendering Method` tab, enable :guilabel:`Default Lighting` and click :guilabel:`Ok`.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000455.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000456.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000457.jpg
   :align: center

Finally, select the :guilabel:`_TERRAIN` and disable the :guilabel:`Edit Poly` and :guilabel:`Volume Select` modifiers by clicking the lightbulb icons next to them. This will restore the sea bed in your viewport.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000458.jpg
   :align: center

Press :kbd:`0` to open the :guilabel:`Render to Texture` window. **Important: Rename the texture** to avoid overwriting your sun and sky terrain lightmap. Backing up your existing lightmaps before generating the water lightmap is also recommended.

All render-to-texture settings are identical to the previous terrain lightmap render. You can use 3ds Max 9 unless you are rendering an 8192x8192 texture, in which case a 64-bit version of Max is required.

.. tip::

   To speed up the process, you can hide your overgrowth and static objects. Since the water light does not cast shadows, their visibility will not affect the render.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000259.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000260.jpg
   :align: center
