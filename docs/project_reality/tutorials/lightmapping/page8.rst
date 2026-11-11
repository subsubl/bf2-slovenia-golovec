
Creating Reference and Shadow Casting Objects
=============================================

Replace current overgrowth meshes, helpers, and other objects with "Reference" objects. These reference objects use transparent materials to cast realistic shadows. Because the currently imported overgrowth meshes lack proper UV coordinates, new meshes must be imported to serve as references.

.. note::

   After reading this section, check the linked forum post, as it contains a 3ds Max scene with many pre-made reference meshes:

   https://www.realitymod.com/forum/f189-modding-tutorials/134649-advanced-3dsmax-lightmapping.html#post2096455

Example: Fixing :file:`af_palmbush_01`. First, import the correct mesh. Navigate to :menuselection:`Bf2 --> Bf2 Utilities` and click :guilabel:`Mesh Import`. Browse to the object's location and select its main :file:`.con` file to import the mesh and its LODs.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000064.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000065.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000066.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000067.jpg
   :align: center

Delete unnecessary LODs and helpers, leaving only the :guilabel:`lod0` mesh. Convert this mesh to an Editable Polygon.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000068.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000069.jpg
   :align: center

Set up the materials. For more information on Multi/Sub-Object materials, refer to `this tutorial <https://www.realitymod.com/forum/f189-modding-tutorials/117705-working-multi-sub-object-materials.html>`_.

Identify the textures used by the object. Open the mesh in a tool like BfMeshView. This object uses a single leaf material with the :file:`leaf_af_palmtree_b_de.dds` texture.

Next, select an unused material slot, click :guilabel:`Standard`, and choose :guilabel:`Multi/Sub-Object`. Click :guilabel:`OK` and rename the new material to something like :guilabel:`Overgrowth`.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000074.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000075.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000077.jpg
   :align: center

Name the first material slot "Bark" and assign a brownish color for easy identification.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000078.jpg
   :align: center

In the parent material, name this sub-material after its texture: ``leaf_af_palmtree_b_de``. Assign that texture to the diffuse slot.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000079.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000080.jpg
   :align: center

Check the :guilabel:`Material ID`s. In :guilabel:`Face Selection` mode, scroll to :guilabel:`Polygon Properties` to verify that the object has two materials: ID :guilabel:`1` for bark and ID :guilabel:`2` for the leaves.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000082.jpg
   :align: center

Note that applying the material now will make the texture visible, but the leaves will not be transparent.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000087.jpg
   :align: center

To achieve transparency, assign an :guilabel:`Opacity Map`. Click :guilabel:`None` next to :guilabel:`Opacity`, select bitmap, and browse to the same texture.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000083.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000084.jpg
   :align: center

The texture reads transparency information from the alpha channel. In the Bitmap Parameters, change the :guilabel:`Mono Channel Output` from RGB Intensity to :guilabel:`Alpha` to make the leaves appear transparent.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000086.jpg
   :align: center

Finally, add backfaces to the leaves.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000096.jpg
   :align: center

While Battlefield 2 automatically draws overgrowth backfaces, 3ds Max requires them to be added manually for correct shadow casting. Select all leaf faces, then click :menuselection:`Detach --> Detach to Element --> Detach as Clone --> Flip` to create flipped copies of the faces.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000097.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000098.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000099.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000100.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000101.jpg
   :align: center

Rename these fixed objects with a ``_REF_`` prefix to identify them as reference geometry. These will be used to replace all other instances of the same object type later.

Continue this process for all overgrowth object types and other objects with transparent materials. Assigning the same materials to objects sharing textures saves time.

Example: Fixing :guilabel:`jungle_palm_small_01`. Follow the same steps, placing the new leaf material (the ``nam_palmtreefrond_01_c`` texture) in the next available material slot. Note that in this instance, the material IDs do not match, and a leaf texture is incorrectly applied to the trunk.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000088.jpg
   :align: center

Examining the face material IDs reveals that one bark section is set to :guilabel:`MatID 2` (a leaf texture). Reassign it to the bark material, :guilabel:`MatID 1`.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000089.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000090.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000092.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000091.jpg
   :align: center

In :guilabel:`kentia_palm_cluster01`, materials are assigned differently: the leaf is :guilabel:`MatID 1` (bark) and the trunk is :guilabel:`MatID 2` (leaf). To fix this, first reassign the leaf faces from :guilabel:`MatID 1` to a new ID (e.g., :guilabel:`MatID 5`), then assign the bark faces to :guilabel:`MatID 1`. Avoid assigning the bark to ID 1 first, as this prevents selecting leaf faces by material ID.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000106.jpg
   :align: center

The process for the Wire Fence series (statics with transparent materials) is similar, with a few key differences: these objects are not overgrowth and already have backfaces, so cloning and flipping faces is not required.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000102.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000103.jpg
   :align: center

First, import the object, delete unnecessary helpers and LODs, leaving only the :guilabel:`lod0` mesh. Convert it to an editable poly and rename it with a ``_REF_`` prefix. Find the transparent texture (``common_alpha_01_de``). Note that the alpha material is the :guilabel:`Detail` material (channel 2), not the :guilabel:`Colour` material (channel 1).

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000104.jpg
   :align: center

Assign materials to the mesh. Assign a non-transparent metal material to the 'Bark' material slot. Even if it is not bark, its non-transparent nature serves the same purpose of blocking light.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000106.jpg
   :align: center

Even with the correct material, the texture may appear incorrect due to improper UVs.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000107.jpg
   :align: center

The texture is a detail map using channel 2 UVs, but it is currently using channel 1. Change the :guilabel:`Map Channel` to 2 to use the correct UVs.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000108.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000109.jpg
   :align: center

Apply the alpha map. To simplify, clone the :guilabel:`Diffuse Material` by dragging and dropping it into another slot and selecting 'copy,' then change it to use the alpha channel.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000112.jpg
   :align: center

Applying the Diffuse Material is not strictly necessary for rendering; only the Opacity material is required. However, applying both makes it easier to verify the results.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000113.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000114.jpg
   :align: center

Consider deleting small pieces of barbed wire on top of the fence. They are too small to cast noticeable shadows and only slow down rendering. This approach can also be applied to other shadow-casting-only objects to improve performance.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000115.jpg
   :align: center

For the civilian car, do not apply transparent materials to the reference mesh. Deleting the windows entirely is simpler and has a marginal impact on lighting, while being easier for the renderer to process. Ensure all faces are set to MatID1 so that if a material is applied, it is only the Bark material.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000116.jpg
   :align: center

Reference meshes are not required for overgrowth or other objects without transparent materials or shadow-casting tweaks. The exception is if an object was imported only as a helper; in that case, replace it with a mesh, but no material fixes are needed if it has no transparent parts.

A total of 45 different reference objects are required for this map.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000118.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000119.jpg
   :align: center
