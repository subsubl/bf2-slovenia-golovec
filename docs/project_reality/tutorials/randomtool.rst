
Using the Random Tool
=====================

:Original Author: azreal64

.. note::

   The original version of this tutorial contained images that are no longer available.

This tutorial describes a technique for using the terrain editor's :guilabel:`Random` tool to add subtle height variation. This method is particularly effective for creating natural terrain in desert environments.

Technique
---------

The :guilabel:`Random` tool can produce extreme results if used without smoothing. Follow these steps to generate subtle terrain bumps:

#. Navigate to the terrain editor and select the :guilabel:`Random` tool.
#. Configure the brush size as required.
#. Set the :guilabel:`Brush Strength` to ``5`` or lower.
#. Click once to apply the random effect, which creates a sharp indentation.
#. Select the :guilabel:`Smooth` tool. Ensure the brush size is slightly larger than the size used for the :guilabel:`Random` tool.
#. Set the smoothing strength between 90% and 100%.
#. Apply the :guilabel:`Smooth` tool over the indentation to refine the terrain.

This process results in subtle, natural-looking terrain features.

.. describe:: Random Tool

   A terrain editor tool that applies random height variations to the terrain surface.

.. describe:: Smooth Tool

   A terrain editor tool used to smooth terrain elevations and reduce sharp features.

.. describe:: Brush Strength

   A parameter that controls the intensity of the height variations applied by the :guilabel:`Random` tool.
