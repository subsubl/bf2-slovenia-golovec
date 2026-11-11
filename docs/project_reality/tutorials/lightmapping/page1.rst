
Introduction
============

:Original Author: Rhino

This tutorial explains refined techniques for lightmapping in 3DsMax for Battlefield 2. As the original 3DsMax lightmapping tutorial from BFEditor.org is no longer available, these methods are documented to assist mappers.

The following section outlines the advantages of using 3DsMax for lightmapping, including benefits introduced in this guide.

* **Speed**: 3DsMax is generally much faster for lightmapping than the BF2 Editor, especially for large, complex maps. This is due to its support for multi-core processing and 64-bit systems. The time saved is significant, even when factoring in the additional steps of importing terrain and objects. This tutorial introduces a method that speeds up the process further by generating all three light types simultaneously.
* **Object Lightmapping**: The BF2 Editor takes approximately 3.5 minutes to generate all LODs for a single complex static. With 3DsMax using Advanced Ray-Traced Shadows, the same task takes only 2.5 minutes, saving one minute per object. This represents approximately 70% of the time required by the BF2 Editor. However, using full Ray-Traced Shadows for maximum quality will take longer, at approximately 6 minutes per object.
* **Terrain Lightmapping**: Time savings are even greater for terrain, as the BF2 Editor struggles to render dense overgrowth. For a sample patch consisting mostly of water with few trees, the BF2 Editor took 11 minutes and 41 seconds. 3DsMax with Advanced Ray-Traced Shadows completed the task in 2 minutes and 38 seconds, which is only 23% of the editor's time. Even with full Ray-Traced Shadows, 3DsMax remains faster at 8 minutes and 20 seconds.
* **Quality**: The lightmaps produced by 3DsMax are of superior quality, especially for overgrowth with transparent leaves (as demonstrated in this tutorial). The final result depends on the selected settings and lighting method.
* **Optimization**: Lightmap sizes are more optimized. Many standard BF2 and Project Reality statics use unnecessarily large lightmap samples. For example, a small house might use a 512x512 texture, which can be reduced to 256x256 in 3DsMax without a noticeable loss in quality, while maintaining a consistent light pixel ratio across the map.
* **Control**: 3DsMax provides significantly more control over lighting and how objects affect the final lightmaps compared to the BF2 Editor.
* **Point Lights**: Creating artificial lights, such as light bulbs, is easier, more flexible, and produces better results in 3DsMax.
* **No Samples Required**: Pre-existing lightmap samples are not required for statics. This allows for the lightmapping of objects from expansion packs. While samples can be generated with tools like Bf2MeshView, this is often a time-consuming process for many objects.
* **Padding**: New scripts provide full lightmap padding, which reduces lighting errors in mipmaps. The BF2 Editor has limited padding capabilities.

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

However, there are several disadvantages to consider:

* **Complexity**: This is a complex process. Users without prior knowledge of 3DsMax and rendering may find it challenging. This tutorial aims to be as straightforward as possible for beginners.
* **Setup Time**: The initial setup can be time-consuming. All static meshes from the map must be imported, and if following this tutorial, overgrowth with transparent leaves must also be set up.
* **Manual Sizing**: Lightmap sizes for each object must be set manually. Fortunately, sizes for most Project Reality statics are already defined. Sizes only need to be defined for objects not on the :guilabel:`Master Lightmap Sizes` list.
* **Child Objects**: Child objects, such as ladders, are not imported with their parent meshes. They must be added manually in 3DsMax to cast shadows. Note that child objects cannot be lightmapped in the BF2 Editor either.
* **Destroyable Objects**: Destroyable objects cannot be lightmapped in 3DsMax without a complicated workaround. It is recommended to generate their lightmaps in the BF2 Editor using settings that mimic 3DsMax.

  If a destroyable object is made non-destroyable through code, its ``geom0`` LODs will import and lightmap correctly. However, the ``geom1`` (wreck) LODs will not be imported. Users must create 8x8 pixel dummy lightmaps for the wreck LODs to ensure the ``geom0`` lightmaps load correctly in-game. This also saves a significant amount of texture space.

Before You Begin
----------------

.. important::

   Before starting this process, ensure the map is complete and thoroughly tested. Having other Project Reality mappers review the map can help identify potential issues. Because making changes to a map after importing it into 3DsMax is difficult, it is recommended to start the process from scratch if issues are found.

It is also not recommended to use 3DsMax lightmapping for a test build of a map. The effort involved may not be justified if subsequent changes are necessary. For test builds, consider using the BF2 Editor on Medium/Low settings or omitting lightmaps entirely. If 3DsMax must be used, skipping steps such as leaf transparency or using Advanced Ray-Traced shadows instead of full Ray-Traced shadows can save time. Note that non-transparent leaves will have lower visual quality compared to lightmaps from the BF2 Editor.

Ensure all prerequisites are met before beginning the process.

Requirements & Tools
--------------------

Tools
^^^^^

* :program:`Battlefield 2 v1.5`
* :program:`BF2 Editor v1.3`: :download:`http://files.ancientdev.com/prbf2/PREditor.zip`
* :program:`Project Reality`: :download:`https://www.realitymod.com/downloads`
* :program:`Working pr_edit Setup`: `<https://www.realitymod.com/forum/f189-modding-tutorials/14468-setting-up-bf2-editor-pr-mapping-modding.html>`_
* :program:`3DsMax9 Version 9+`
* :program:`PR:BF2 3DsMax9 Tools`: `<https://www.realitymod.com/forum/showthread.php?t=145720>`_
* :program:`Adobe Photoshop`: `<https://www.adobe.com/products/photoshop.html>`_
* A Text Editor

  * :program:`Notepad++`: :download:`https://notepad-plus-plus.org/downloads/`
  * :program:`Visual Studio Code`: :download:`https://code.visualstudio.com/download`

Materials
^^^^^^^^^

* A Decent Computer

  A better system will allow for faster lightmap generation and more RAM will provide greater stability when generating large terrain lightmaps.

* A Finalised Map Ready for Lightmapping


.. important::

   Ensure all of the above are installed and working before starting this tutorial.

.. note::

   This tutorial uses a :file:`pr_repo` mod connected to an SVN Repository; ignore any unusual folder icons. The working mod is referred to as :file:`pr_edit`. If 'pr_repo' appears in screenshots, substitute it with the appropriate working mod name (e.g., :file:`pr_edit`).
