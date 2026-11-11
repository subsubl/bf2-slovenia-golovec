
Converting Overgrowth to Static
===============================

3DsMax cannot directly import overgrowth placed with the in-game tool. To work around this, convert all overgrowth objects into static objects, which can then be imported into 3DsMax.

.. important::

   Before starting, create a backup of the :file:`Staticobjects.con` file, which contains all buildings and props. Rename the backup to something like :file:`Staticobjects_Final_YYYY-MM-DD.con`.

Next, clear the contents of the original :file:`Staticobjects.con`. This can be done in the editor by selecting all objects in the main layer and deleting them. This may take some time. Ensure no static objects remain in any other layers. Alternatively, open the file in a text editor, delete all its contents, and reload the editor. After clearing it, the :file:`staticobjects.con` file should only contain the "run" lines for the overgrowth.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000348.jpg
   :align: center

The next step can be tricky. A common bug after lightmapping may disable the view, making the following steps more difficult.

First, position the camera to view the entire map. It may be necessary to increase the editor's view distance settings. Place a small, simple object, such as a 1-meter crate, anywhere on the map and lightmap it on low settings. Delete the object immediately after lightmapping is complete.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000002.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000003.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000004.jpg
   :align: center

Overgrowth is now converted to static objects and can be selected, even if the view is disabled. Drag a selection box over the entire map. If the view is disabled, the selection box may not be visible. In that case, click and hold in one corner for a few seconds before dragging to allow the editor time to register the input, as it may be running slowly. Selecting all objects may take some time. "[Tweaker] Load Object (Object)" messages should appear repeatedly in the output bar.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000006.jpg
   :align: center

Once all overgrowth is selected, check the :guilabel:`IsSaveable` box in the tweaker bar (which will turn green) and apply this setting to all selected objects:

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000007.jpg
   :align: center

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000008.jpg
   :align: center

After that, save the objects.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000009.jpg
   :align: center

The :file:`staticobjects.con` file should now contain all overgrowth objects.

.. image:: https://media.realitymod.com/tutorials/Adv_3DsMax_LMing/Adv_3DsMax_LMing_000010.jpg
   :align: center

Rename this file to :file:`Staticobjects_Overgrowth.con`. Finally, restore the original :file:`Staticobjects.con` backup (the one containing buildings) to its original location.
