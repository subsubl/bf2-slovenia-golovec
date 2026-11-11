
Replacing Objects with Reference Objects
========================================

Replace all types of overgrowth and other objects with the newly created reference objects, one type at a time.

First, unhide the Overgrowth group, ungroup it, and unhide the Overgrowth Helpers layer. Unhide any other objects intended for replacement that do not require lightmaps. Keep all other objects hidden, except for the reference meshes.

Start by replacing :guilabel:`af_palmbush_01`. Select the object by name, excluding the ``=0`` suffix, to ensure the helpers are also selected. The reference object, using the prefix ``_REF_``, will remain unselected.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000120.jpg
   :align: center

#. Go to :menuselection:`MaxScript --> Run Script`.
#. Navigate to the :file:`bf2` folder within your scripts folder and select the :file:`instance replace.ms` script, which is included in the PR:BF2 3DsMax9 v0.40 Tools.
#. A small window will appear. Click :guilabel:`Pick Master` and press :kbd:`H` to select by name.
#. Select the reference object you want to use for replacement, which in this case is the :guilabel:`_REF_af_palmbush_01` mesh.
#. Click :guilabel:`Make Instances` to replace all selected :guilabel:`af_palmbush_01` objects with the :guilabel:`_REF_af_palmbush_01` mesh.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000121.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000122.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000123.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000124.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000125.jpg
   :align: center

After replacement, apply the :guilabel:`Overgrowth` material to the selection.

Note that objects like :guilabel:`civi car 1` do not require this material; applying it may cause issues because the :guilabel:`MatID's` do not match the bark material. Once applied, the objects should display transparent leaves.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000126.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000127.jpg
   :align: center

Repeat this process until all old objects are replaced with reference objects. Upon completion, the scene should resemble the following.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000128.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000129.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000130.jpg
   :align: center

If viewport performance decreases due to transparent textures, temporarily assign a blank material to them. The correct material must be reapplied before lightmapping. To ensure compatibility, verify that all objects, such as logs and civilian cars, are compatible with the material.

To ensure compatibility, search for all logs using ``*log``. This selects all objects with 'log' in their name (e.g., :guilabel:`nc_deadlog01` and :guilabel:`me_deadlog01`).

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000131.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000132.jpg
   :align: center

Next, apply a :guilabel:`Material` modifier to all selected objects and set it to apply :guilabel:`Material 1` to all faces.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000133.jpg
   :align: center

Repeat this for :guilabel:`civiliancar1`. Applying a blank material to all overgrowth objects will turn them gray and increase FPS.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000134.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000135.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000136.jpg
   :align: center

Reapplying the material to the entire selection will make the cars and logs appear brown, as they will now use the bark material.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000137.jpg
   :align: center

Alternatively, disable the :guilabel:`show in viewport` button for each material. While this should still allow transparent leaves to render during lightmapping, it may be slower than swapping materials, depending on system performance and the number of transparent objects.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000138.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000139.jpg
   :align: center

Finally, set these objects to a 'Green' color for easy distinction in wireframe view. Add all these objects, excluding the reference objects, to the :guilabel:`Overgrowth Helpers` layer (renamed to *Overgrowth*).

Group these objects into an :guilabel:`Overgrowth` group to maintain an organized selection list.

Repeat this for the reference objects, using a different color, such as yellow.

#. Create a new :guilabel:`References` layer for them.
#. Exclude the layer from rendering by clicking the teapot icon next to it until it disappears.
#. Hide that layer.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000140.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000141.jpg
   :align: center

Reference meshes are not required for overgrowth or other objects without transparent materials or shadow-casting tweaks. The exception is if an object was imported only as a helper; in that case, replace it with a mesh, but no material fixes are needed if it has no transparent parts.

A total of 45 different reference objects are required for this map.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000142.jpg
   :align: center

We should not need them anymore, but it is best to keep them in the scene in case we do. Since all the objects are now instanced to them, any tweaks can be made to the main reference object and will be applied to all the others.
