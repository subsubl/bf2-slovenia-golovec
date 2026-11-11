
Full Object Lightmaps
=====================

For optimal speed and stability, it is recommended to render full lightmaps in a 64-bit version of 3ds Max (later than Max 9). To do this, install the :download:`PR:BF2 3DsMax9 Tools <https://www.realitymod.com/forum/f189-modding-tutorials/134050-pr-bf2-3dsmax9-tools-v0-40-a.html>` into your newer version of Max. While some scripts like importing and exporting may not be compatible, the lightmap generation scripts have been tested on 3ds Max 2010 and 2012 and should function correctly.

.. warning::

   Always back up your Max scene and save a separate version to be loaded by a newer version of Max, as files saved in newer versions are not backward compatible.

To maximize performance, restart your computer and close all unnecessary programs to free up as much CPU and RAM as possible. Background applications can consume resources and slow down the lightmap generation process.

Once your system is optimized, start your chosen version of 3ds Max. Navigate to :menuselection:`BF2 --> Bf2 Lightmapping` and click :guilabel:`Render All Lightmaps`.

Before rendering, ensure the following settings are configured:

* The :guilabel:`Light Pass` dropdown is blank (this renders all light passes simultaneously).
* The :guilabel:`Specific LOD` setting is set to :guilabel:`All`.

If you need to skip previously generated lightmaps, select the :guilabel:`Resume` button. This feature checks if an object's LOD already has a lightmap in your :guilabel:`Temp` folder and skips it if found, which is useful if the system crashes during the process.

.. note::

   Ensure your temporary directory is correct and your lightmap size file is loaded before starting the render.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000255.jpg
   :align: center

In this tutorial, rendering approximately 200 objects with :guilabel:`Adv. Ray Traced` shadows took under 7 hours (averaging about 2 minutes per object).

The following images show the results of the object lightmapping. Note that the terrain continues to use medium-quality editor lightmaps:

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000223.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000224.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000225.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000226.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000227.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000228.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000229.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000230.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000231.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000232.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000233.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000234.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000235.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000236.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000237.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000238.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000239.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000240.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000241.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000242.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000243.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000244.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000245.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000246.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000247.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000248.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000249.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000250.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000251.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000252.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000253.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000254.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000256.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000257.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000258.jpg
   :align: center

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
