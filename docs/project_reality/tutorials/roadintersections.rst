
Road Intersections
==================

:Original Author: [R-DEV] Rhino (Retired)

.. important::

   The original version of this tutorial contains images that are no longer available.

This tutorial describes how to place and configure road intersections to ensure clean, professional road layouts.

Overview
--------

A road intersection is a static object that connects roads at crossing points, preventing texture gaps or misalignment. Common types include basic cross intersections, T-junctions, and 45-degree intersections.

Prerequisites
-------------

* :program:`Battlefield 2 Editor v3`
* A functional map
* Optional: :program:`Photoshop`, :program:`GIMP`, or :program:`3ds Max` (version 8 or 9) for custom road textures and intersections

Step 1: Planning
----------------

Load the map in the :guilabel:`Level Editor`. Plan the road layout before placing intersections and roads to prevent unnecessary rework.

Step 2: Placing Intersection Statics
------------------------------------

Intersection static objects are located in :file:`/Objects/Roads/Statics/`. Custom intersection types for specific angles are located in the :file:`/pr/` subfolder.

#. Select the desired intersection static (e.g., :file:`cross_intersection`).
#. Drag and drop the static into the map.
#. Position the static accurately.

Step 3: Connecting Roads
------------------------

Use the :guilabel:`Road` tool to connect intersections.

#. Place splines to connect road intersections end-to-end. Ensure the road template matches the intersection template.
#. Offset the initial and final splines slightly from the center of the road to improve draw quality near the junction.
#. Position the road ends immediately before the center of the intersection and overlap the junction geometry.
#. Ensure the road does not pass through the center of the intersection to avoid edge misalignment.
#. If working on a grid-based map, align intersections and roads to the grid to enable spline snapping and improve alignment speed.

Step 4: Dirt Track Intersections
--------------------------------

Dirt tracks do not require static intersection objects. Instead, overlap dirt roads across tarmac or other dirt roads.

Control the stacking order using the following parameter:

.. describe:: Prio (Priority)

   A configuration parameter in the road file that determines the stacking order of overlapping roads.

   * Higher priority values appear on top.
   * Lower priority values appear below.

For example, set the tarmac road priority to ``0`` and the intersecting dirt road priority to ``1`` or higher to ensure the dirt road appears above the tarmac road. To create a junction, use a connecting dirt road segment with a lower priority than the main road.

Advanced Techniques
-------------------

Custom Road Textures
^^^^^^^^^^^^^^^^^^^^

If custom road textures lack corresponding intersection textures, use one of the following methods:

#. **Texture Suffixes**: Apply a map-specific texture suffix to create a new road template (e.g., :file:`Tarmac_mirror_muttrah.dds`).
#. **Cloning Statics**: Clone an existing intersection static, rename it, and use :file:`BF2Materials.exe` to update the texture paths.

Creating New Intersections
^^^^^^^^^^^^^^^^^^^^^^^^^^

New intersections are flat models with assigned textures. Once exported to :file:`objects/roads/statics/`, they function identically to standard road intersections.
