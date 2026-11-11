
Cleaning Up Objects
===================

Many imported objects will not need lightmaps, should not cast shadows, or cannot be lightmapped. Sort through these objects to clean up the scene. This process involves reviewing each unique object type, rather than every single instance.

First, hide all objects in the scene. Right-click in the viewport and select :guilabel:`Hide Unselected`. Then, right-click again and choose :guilabel:`Unhide By Name` to select and unhide specific objects to modify. For example, the :guilabel:`Bundled Mesh` :guilabel:`civiliancar1` cannot be lightmapped but should cast a shadow. It also includes extra meshes for first-person and wreck views that should be removed.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000044.jpg
   :align: center

Next, select and delete the ``geom0`` (first-person mesh) and ``geom2`` (wreck mesh) sub-trees. This can be done by searching for ``geom0`` with :guilabel:`select sub tree` enabled, deleting the results, and then repeating the process for ``geom2``. This leaves only ``geom1``, which is the visible mesh in-game.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000046.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000047.jpg
   :align: center

Select the object's name (in this case, "0"), click :guilabel:`inverse` to select all associated helpers, and delete them, leaving only the mesh.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000048.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000049.jpg
   :align: center

In this example, the mesh name is incorrect. Select all the meshes and go to :menuselection:`Tools --> Rename Objects`. Rename it to the proper name, :guilabel:`civiliancar1`.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000050.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000051.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000053.jpg
   :align: center

Another example involves static overgrowth in :file:`staticobjects.con`. Remove the LODs and helpers for these objects so the script does not attempt to lightmap them and to prevent the LODs from casting shadows.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000054.jpg
   :align: center

Follow the same basic steps. Select the helpers for deletion by unchecking `geom` from the selection list.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000055.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000056.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000057.jpg
   :align: center

The runway paving slabs do not need lightmaps and should not cast shadows, so delete them and their helpers entirely.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000058.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000059.jpg
   :align: center

The wire fence series cannot be lightmapped correctly due to improper lightmap UVs, but they should cast shadows. Later, the wire will be set to transparent so it does not cast a solid shadow. For now, delete all but the :guilabel:`lod0` mesh.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000060.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000061.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000062.jpg
   :align: center

Finally, select all cleaned-up objects that will only be used for casting shadows and group them into a new group called ``_OVERGROWTH``. While some objects, like the car, are not technically overgrowth, most are.

.. note::

   This group does not include the overgrowth helpers imported earlier. It only contains the overgrowth and other objects sorted from the main statics.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000063.jpg
   :align: center
