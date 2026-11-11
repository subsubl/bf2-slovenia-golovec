
Importing Sun & Preparing your Lights
=====================================

To begin adding light to the scene, load the sun from your sky settings. Navigate to :menuselection:`BF2 --> BF2 Lightmapping --> Load Sun`. Browse to your map folder, select the :file:`sky.con` file, and a direct light will be created at the same position as your in-game sun.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000171.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000172.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000173.jpg
   :align: center

For maps larger than 2km, the light may be created too close to the terrain. Since the script is optimized for 2km maps or smaller, the far sides of a larger map may not be lit correctly. For 4km or larger maps, move the sun further away without changing its rotation.

#. Select the :guilabel:`BF2_SunLight` object.
#. Use the :guilabel:`Move Tool` (:kbd:`W`).
#. Switch to :guilabel:`Local Transformation` mode so the gizmo aligns with the sun's rotation.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000175.jpg
   :align: center

At the bottom of the screen, click the :guilabel:`Absolute Mode Transform Type-In` button until it turns yellow, indicating it is in :guilabel:`Offset Mode`. In the :guilabel:`Z` axis box, enter :guilabel:`10000` (for a 4km map; larger maps require a greater distance). This moves the sun 10,000 units (1km) along its Z-axis.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000178.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000179.jpg
   :align: center

Configure the sun's light settings. There are two primary shadow casting methods for sun lights in 3ds Max: :guilabel:`Ray Traced Shadows` and :guilabel:`Adv. Ray Traced`. Both methods share several common settings.

#. Select the sun and navigate to the :guilabel:`Modifier` tab. Check the :guilabel:`On` box under :guilabel:`Shadows`. Set the drop-down menu to :guilabel:`Shadow Map` for now.
#. Under :guilabel:`Intensity/Color/Attenuation`, set the :guilabel:`Light Multiplier` to :guilabel:`2` for a sunny map or :guilabel:`1` for a cloudy map.

.. warning::

   Do not set the multiplier below 1. It is easier to darken a map via the map's light settings than through lightmaps. For night maps without a moon, you can remove the sun light by setting its color to black.

#. Change the :guilabel:`Light Colour` to :guilabel:`0, 255, 0` (RGB). This ensures that sun light uses the green channel in the RGB lightmap, allowing all light types to be generated simultaneously.
#. In the :guilabel:`Directional` parameters, if working with a 4km map, set the :guilabel:`Hotspot/Beam` to :guilabel:`30000` (or more for larger maps) to ensure full map coverage. Verify the remaining settings against the images below.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000181.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000180.jpg
   :align: center

Choose the shadow type that best suits your map and hardware capabilities.

Ray-Tracing Comparison
----------------------

.. list-table::
   :header-rows: 1
   :widths: auto
   :align: center

   * - BF2 Editor (Final Quality)
     - 3DsMax (Ray-Traced Shadows)
     - 3DsMax (Advanced Ray-Traced)
   * - |image1|
     - |image2|
     - |image3|
   * - |image4|
     - |image5|
     - |image6|
   * - |image7|
     - |image8|
     - |image9|

.. |image1| image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/method_examples/Adv_3DsMax_LMing_eg15_terrain_BF2Editor.jpg
.. |image2| image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/method_examples/Adv_3DsMax_LMing_eg15_terrain_RayTracedShadows.jpg
.. |image3| image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/method_examples/Adv_3DsMax_LMing_eg15_terrain_AdvRayTraced.jpg
.. |image4| image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/method_examples/Adv_3DsMax_LMing_eg17_terrain_BF2Editor.jpg
.. |image5| image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/method_examples/Adv_3DsMax_LMing_eg17_terrain_RayTracedShadows.jpg
.. |image6| image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/method_examples/Adv_3DsMax_LMing_eg17_terrain_AdvRayTraced.jpg
.. |image7| image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/method_examples/Adv_3DsMax_LMing_eg14_terrain_BF2Editor_LM.jpg
.. |image8| image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/method_examples/Adv_3DsMax_LMing_eg14_terrain_RayTracedShadows_LM.jpg
.. |image9| image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/method_examples/Adv_3DsMax_LMing_eg14_terrain_AdvRayTraced_LM.jpg

Ray-Traced Shadows
------------------

Ray-Traced Shadows is a high-quality but slow rendering option. It is recommended for final, thoroughly tested maps, as any changes to lightmaps will require a full re-render.

On complex objects, lightmaps take approximately **6 minutes per object** (including all LODs) for high-resolution settings. This is about **3 times slower** than :guilabel:`Adv. Ray Traced` and twice as slow as the BF2 Editor's :guilabel:`Final Quality` setting.

However, for terrain with heavy overgrowth, :guilabel:`Ray Traced Shadows` is more efficient than the BF2 Editor. For example, a patch that took 11 minutes and 41 seconds in the editor can be rendered in approximately **8 minutes and 20 seconds** using :guilabel:`Ray Traced Shadows` in 3ds Max.

The resulting shadow quality is significantly superior to both :guilabel:`Adv. Ray Traced` and the BF2 Editor.

To use this mode, keep all previous settings and change the :guilabel:`Shadows` drop-down to :guilabel:`Ray Traced Shadows`.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000181.jpg
   :align: center

Adv. Ray-Traced Shadows
-----------------------

Adv. Ray-Traced Shadows is a medium-quality, faster rendering option. It is ideal if you lack the hardware for :guilabel:`Ray Traced Shadows` or if you plan to make further changes to your map that require re-lightmapping.

On complex objects, high-resolution lightmaps take approximately **2 minutes and 30 seconds per object** (including all LODs). This is roughly **1/3 of the time** required for :guilabel:`Ray Traced Shadows` and nearly half the time of the BF2 Editor's :guilabel:`Final Quality` setting.

For terrain, it is considerably faster, taking about **2/9th** of the time used by the BF2 Editor (e.g., 2 minutes and 38 seconds compared to 11 minutes and 41 seconds).

While the quality is not as high as :guilabel:`Ray Traced Shadows` and may occasionally be comparable to or slightly worse than the BF2 Editor (especially regarding transparent leaf rendering), it still generally offers better quality than the BF2 Editor, particularly in areas with significant overgrowth.

To use this mode, keep all previous settings and change the :guilabel:`Shadows` drop-down to :guilabel:`Adv. Ray Traced`. In the :guilabel:`Optimizations` rollout, enable :guilabel:`Transparent Shadows` (for transparent leaf textures) and set the :guilabel:`Antialiasing Threshold Colour` to 100% black.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000222.jpg
   :align: center

For this tutorial, :guilabel:`Adv. Ray Traced` shadows will be used to balance quality and rendering speed.

Main Tutorial
-------------

Import Lights
^^^^^^^^^^^^^

To begin, import the sky lights using the recommended template for this tutorial. This template provides a solid starting point for tweaking.

#. Download the template: :download:`Lightmaps_Sky_Light_Template.zip <https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Lightmaps_Sky_Light_Template.zip>`
#. Navigate to :menuselection:`File --> Merge`, select the downloaded file, and import all lights into your map.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000182.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000183.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000184.jpg
   :align: center

Configure Lights
^^^^^^^^^^^^^^^^

The template contains two primary lights:

.. describe:: _Sky01
   
   The main skylight. It produces realistic light bouncing, illuminating outdoors while allowing light to filter into interiors through windows and doors.

.. describe:: _Ambient_Fill_light
   
   Provides flat illumination across the entire map, from caves to skyscrapers. This ensures building interiors are not pitch black.

Adjust the :guilabel:`_Sky01` and :guilabel:`_Ambient_Fill_light` multipliers to control interior brightness. For brighter interiors, increase the :guilabel:`_Ambient_Fill_light` multiplier and decrease the :guilabel:`_Sky01` multiplier.

Both skylights use a color of :guilabel:`0, 0, 255` (100% Blue) to facilitate simultaneous generation of all light types by utilizing the blue channel in the lightmap.

Next, configure :guilabel:`Point Lights` (e.g., lamp posts). For this tutorial, a large omni light will be created in the lighthouse:

#. Click the :guilabel:`Object Creation` button in the top right.
#. Select the :guilabel:`light` icon, then click the :guilabel:`Omni` button.
#. Place the light in the lighthouse.
#. Enable shadows. Select the same shadow type used for the sun (e.g., :guilabel:`Adv. Ray Traced`).
#. Set the multiplier to :guilabel:`1` and the light color to :guilabel:`255, 0, 0` (100% Red).

   .. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000185.jpg

   .. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000190.jpg

   .. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000186.jpg

#. Configure the decay type:

   * :guilabel:`Inverse Square` starting at 100 (10m).
   * :guilabel:`Far Attenuation` starting at 200 (20m) and ending at 1000 (100m).
   * Leave all other settings at default.

.. tip::

   These settings can be fine-tuned based on desired light intensity and distance. Achieving the perfect balance may require trial and error via viewport renders or test lightmap renders.

Finally, a lighting template for the carrier can also be applied. This template includes three types of lights: two :guilabel:`Spot Light` types and one :guilabel:`Omni Light` type. Since these are instances, changing one will update all others.

To use this template, download it here and align it to the bridge: :download:`Lightmaps_Carrier_Lights_Template.zip <https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Lightmaps_Carrier_Lights_Template.zip>` (Note: This is configured for the HMS Invincible and may vary for the USS Essex).

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000188.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000189.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000191.jpg
   :align: center

.. note::

   You can set up light templates for specific static object types (e.g., a set of lights for building bulbs) and apply them to all instances of that static. If you are interested in learning how to do this, please let us know.
