
Using the Level Brush Tool
==========================

:Original Author: Outlawz7

The "Level Brush" (or "Paint" mode) is a tool within the BF2 Editor's Level Editor plugin. It enables the efficient placement of repetitive assets by allowing users to "paint" collections of objects, known as brushes, onto a map. This method is often more efficient than manual :guilabel:`Move` and :guilabel:`Rotate` operations.

.. image:: https://i.imgur.com/wMXOcI7.jpg
   :align: center

Tool Overview
-------------

The Level Brush tool allows you to paint brushes onto a map via mouse clicks or dragging. You can define minimum and maximum thresholds for position, rotation, and scale to introduce randomization to each brush instance.

Saved brushes are stored as individual files in the BF2 Editor's directory: :file:`bf2editor\Content\LevelEditor\LevelBrushes`.

.. figure:: https://i.imgur.com/dGy3TTk.jpg
   :align: center

   Sidebar Controls

.. describe:: Active Brush

   Displays the currently selected brush.

.. describe:: Define Brush

   Creates a new brush from one or more selected static objects. You will be prompted to provide a name.

.. describe:: Add To Brush

   Appends selected static objects to the currently active brush. Note that new objects are added at a 0/0/0 position and may require manual adjustment.

.. describe:: Paint Mode

   Toggles the paint functionality in the editor viewport.

Brushes are accessible from the bottom of the Resources bar.

.. figure:: https://i.imgur.com/xavoodj.jpg
   :align: center

   Brush location in the Resources bar.

.. figure:: https://i.imgur.com/Ztzqjaj.jpg
   :align: center

   TweakBar settings.

.. describe:: Spacing

   Defines the minimum distance between each new object instance when painting.

.. describe:: SnapToGround

   When enabled, objects attempt to snap to the ground surface. If disabled, objects are placed relative to their pivot point or center, which may result in objects being partially buried.

Randomization Controls
----------------------

You can define ranges to introduce variety into your brush instances:

* **RandomPositionMin / Max**
* **RandomRotationMin / Max**
* **RandomScaleMin / Max**

For rotation, use values between -180 and 180, as the engine converts all values to this range. Note that the X and Y axes are swapped for both position and rotation; specifically, the "Y" value acts as the vertical axis.

.. image:: https://i.imgur.com/ZmS8Io2.jpg
   :align: center

.. code-block:: text
   :caption: Example randomization settings

   LevelBrush.RandomPositionMin 0.000/0.000/0.000
   LevelBrush.RandomPositionMax 22.000/22.000/22.000
   LevelBrush.RandomRotationMin 0.000/0.000/0.000
   LevelBrush.RandomRotationMax 22.000/22.000/22.000
   LevelBrush.RandomScaleMin 0.000/0.000/0.000
   LevelBrush.RandomScaleMax 55.000/55.000/55.000

Operational Notes and Limitations
---------------------------------

Item Management
   An individual static object within a brush is referred to as an "Item."

Deletion
   Items and brushes cannot be deleted directly through the editor interface. You must manually edit or delete the brush files in the file system.

Overlapping
   The tool does not perform collision detection with existing objects. Avoid painting brushes in the same location, as overlapping objects create significant performance overhead due to redundant rendering.

Editing Behavior
   When editing the values of an item within a brush, the editor may continue to display the previous values in the interface, even though the changes are correctly saved to the file.

Recommendation
--------------

While the dedicated Overgrowth tool is preferred for vegetation, the Level Brush tool is highly effective for the rapid placement of objects with randomized rotation and positioning, such as rocks or debris.

.. image:: https://i.imgur.com/5mcFey2.jpg
   :align: center

.. image:: https://i.imgur.com/2havgDv.jpg
   :align: center
