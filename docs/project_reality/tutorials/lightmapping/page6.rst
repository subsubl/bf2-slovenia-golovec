
Importing Overgrowth into 3DsMax
================================

After restarting the computer, import the overgrowth. To save significant time, first navigate to the :file:`EA GAMES\\Battlefield 2\\mods\\pr_edit\\Objects` folder. Temporarily move the :file:`vegetation` folder to a location outside of the :file:`pr_edit` directory. This prevents the import script from finding the object meshes and instead creates a helper for each one.

.. important::

   Create a backup of the :file:`Staticobjects.con` file before proceeding.

After moving the folder, open a new 3DsMax scene with the same unit setup as the previous scene. Follow the same process for importing statics, but select the overgrowth :file:`Staticobjects.con` file (e.g., :file:`Staticobjects_Overgrowth.con` from the previous step).

Using a new, empty scene helps the import script run more efficiently, as it can slow down in a scene that is already populated. The imported helpers will be merged into the main scene later.

Once the import is complete, the scene will contain a collection of helpers:

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000032.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000038.jpg
   :align: center

Save this new scene with a name indicating it contains the overgrowth, such as :file:`YourMapName_Overgrowth.max`.

Create a backup of this file. Then, move the :file:`vegetation` folder back to its original location in :file:`\\pr_edit\\Objects`.

Open the main lightmapping scene containing the terrain and statics. Use :menuselection:`File --> Merge` and select the scene with the imported overgrowth helpers. Click :guilabel:`All` to select everything, then click :guilabel:`Ok` to merge the helpers into the current scene.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000037.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000039.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000040.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000041.jpg
   :align: center

.. important::

   Add the newly imported helpers to a new layer named ``Overgrowth Helpers``.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000042.jpg
   :align: center

Finally, save the lightmapping scene and create a backup.
